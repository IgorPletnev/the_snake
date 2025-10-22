import pygame
from random import randint

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 0, 255)
SPEED = 17


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для других игровых объектов."""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Абстрактный метод для отрисовки объектов."""
        pass


class Apple(GameObject):
    """Класс для представления яблока в игре."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Случайное положение яблока в пределах игрового поля"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, унаследованный от GameObject, описывающий змейку"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки после нажатия клавиши"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки и удаляя хвост при необходимости"""
        # Получаем текущую позицию головы
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        # Вычисляем новую позицию головы с учетом границ экрана
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        # Сохраняем последний сегмент для затирания
        self.last = self.positions[-1] if len(self.positions) > 0 else None

        # Вставляем новую позицию головы в начало списка
        self.positions.insert(0, new_position)

        # Удаляем последний элемент если длина змейки не увеличилась
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовывает змейку на экране, затирая след"""
        # Отрисовка всех сегментов змейки
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для изменения направления движения змейки"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def show_game_over():
    """Отображает сообщение 'Game Over' на экране"""
    font = pygame.font.Font(None, 100)
    text = font.render('GAME OVER', True, (255, 156, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)


def main():
    """Основная функция игры, содержащая главный игровой цикл"""
    pygame.init()
    snake = Snake()
    apple = Apple()
    # Основной игровой цикл
    while True:

        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убеждаемся, что яблоко не появилось внутри змейки
            while apple.position in snake.positions:
                apple.randomize_position()

        # Проверка столкновения змейки с собой
        if snake.get_head_position() in snake.positions[1:]:
            show_game_over()
            snake.reset()
            apple.randomize_position()

        # Отрисовка игровых объектов
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()

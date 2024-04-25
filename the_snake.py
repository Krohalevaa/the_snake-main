from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет по умолчанию
DEFAULT_COLOR = (100, 100, 100)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_quit(event):
    """Доп функция для функции обработки действий пользователя."""
    if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit


def handle_keys(game_object):
    """Функция обработки действий пользователя.
    Обрабатывает нажатия клавиш для изменения направления
    движения змейки.
    """
    for event in pygame.event.get():
        handle_quit(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Класс, в котором отображаются объекты игрового поля."""

    def __init__(self, position=(0, 0)) -> None:
        self.position = position
        self.body_color = DEFAULT_COLOR

    def draw(self):
        """Нарисовать объект ЦЕЛИКОМ"""
        pass


class Apple(GameObject):
    """Класс, в котором описываются все необходимое для работы яблока"""

    def __init__(self) -> None:
        super().__init__((0, 0))
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Метод который устанавливает случайное положение яблока
        в пределах игрового поля
        """
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Метод отрисовки яблока на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, в котором описываются все необходимые компоненты
    для работы змейки
    """

    def __init__(self) -> None:
        super().__init__((GRID_WIDTH // 2 * GRID_SIZE,
                          GRID_HEIGHT // 2 * GRID_SIZE))
        self.direction = RIGHT
        self.length = 1
        self.positions = [self.position]
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Этот метод обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, обновляющий позицию змейки."""
        s_head_x, s_head_y = self.positions[0]
        dx, dy = self.direction
        new_s_head = ((s_head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                      (s_head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new_s_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_s_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self):
        """Метод, который отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def main():
    """Функция, описывающая работу основного игрового цикла"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

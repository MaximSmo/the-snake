from random import choice, randint

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

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Родительский класс игровых объектов 'змейка' и яблоко'.

    Инициализируются общие атрибуты: кооординаты на игровом поле и цвет.
    Хранит общий метод отрисовки одной ячейки draw_rec, куда передаем
    координаты ячейки и цвет.
    """

    def __init__(self):
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw_rec(self, position, color):
        """Рисует одну ячейку с заданным цветом и координатами."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Игровой объект 'яблоко'.

    Яблоко появляется в случайной свободной клетке поля. По умолчанию
    инициализируется с красным цветом.

    Атрибуты:
        position (list): Координаты яблока на игровом поле [x, y].
        body_color (tuple): Цвет яблока в формате RGB.
    """

    def __init__(self, body_color: tuple = APPLE_COLOR):
        super().__init__()
        self.body_color = body_color

    def randomize_position(self, snake):
        """Задает яблоку случайные координаты на свободной клетке."""
        while self.position in snake:
            self.position = [
                randint(0, int(SCREEN_WIDTH / GRID_SIZE) - 1) * GRID_SIZE,
                randint(0, int(SCREEN_HEIGHT / GRID_SIZE) - 1) * GRID_SIZE,
            ]

    def draw(self):
        """Рисует яблоко."""
        self.draw_rec(self.position, self.body_color)


class Snake(GameObject):
    """Игровой объект 'змейка'.

    В начале игры змейка длиной 1 стоит в центре поля и ползет направо.

    Атрибуты:
        length (int): Текущая длина змейки.
        positions (list): Координаты всех сегментов змейки,
            первый элемент - голова.
        direction (tuple): Текущее направление движения.
        next_direction (tuple): Следующее направление движения после
            нажатия клавиши, либо None.
        body_color (tuple): Цвет змейки в формате RGB.
        last (list): Координаты последнего удаленного сегмента хвоста.
    """

    def __init__(self, body_color: tuple = SNAKE_COLOR):
        super().__init__()
        self.reset()
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = body_color
        self.last = 0

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Меняет координаты головы змейки согласно направлению движения."""
        dx, dy = self.get_head_position()
        move_x, move_y = self.direction
        self.positions.insert(0, [
            (dx + move_x * GRID_SIZE) % SCREEN_WIDTH,
            (dy + move_y * GRID_SIZE) % SCREEN_HEIGHT,
        ])

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Рисуем тело змейки с первого по последний сегмент."""
        for position in self.positions:
            self.draw_rec(position, self.body_color)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, next_direction):
        """Обновляет направление движения змейки."""
        if next_direction:
            self.direction = next_direction

    def reset(self):
        """Сбрасывает змейку в начальное состояние.

        Змейка возвращается в центр поля с длиной 1, а направление
        движения выбирается случайно.
        """
        self.length = 1
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def handle_keys(game_object):
    """Управление игрой клавишами."""
    dict_of_direction = {
        (pygame.K_UP, RIGHT): UP,
        (pygame.K_RIGHT, DOWN): RIGHT,
        (pygame.K_DOWN, LEFT): DOWN,
        (pygame.K_LEFT, UP): LEFT,
        (pygame.K_UP, LEFT): UP,
        (pygame.K_RIGHT, UP): RIGHT,
        (pygame.K_DOWN, RIGHT): DOWN,
        (pygame.K_LEFT, DOWN): LEFT,
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            try:
                game_object.update_direction(
                    dict_of_direction[event.key, game_object.direction]
                )
            except KeyError:
                break


def main():
    """Запускает игру и основной игровой цикл.

    В каждом кадре обрабатываются нажатия клавиш, змейка двигается,
    проверяется столкновение с телом (тогда игра сбрасывается)
    и съедание яблока (тогда змейка растет). После этого объекты
    отрисовываются на экране.
    """
    pygame.init()
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        snake_head = snake.get_head_position()

        if snake_head in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        if snake_head == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pygame.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == '__main__':
    main()

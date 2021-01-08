import pygame
import random
import sqlite3


class Tetris:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.current_figure = (None, None)
        self.cell_size = cell_size
        self.score = 0

    def add_figure(self, figure_type=None):
        col = random.randint(0, self.width - 1)
        self.current_figure = (0, col)
        self.board[0][col] = 1

    def move_figure(self, direction='down'):
        row, col = self.current_figure
        if row is None:
            return

        if direction == 'down':
            if row + 1 >= self.height:
                return
            self.current_figure = (row + 1, col)
            self.board[row][col] = 0
            self.board[row + 1][col] = 1
        elif direction == 'left':
            if row + 1 == self.height or col - 1 < 0:
                return
            self.current_figure = (row, col - 1)
            self.board[row][col] = 0
            self.board[row][col - 1] = 1
        elif direction == 'right':
            if row + 1 == self.height or col + 1 >= self.width:
                return
            self.current_figure = (row, col + 1)
            self.board[row][col] = 0
            self.board[row][col + 1] = 1

    def tick(self):
        row, col = self.current_figure
        if row is None:
            self.add_figure()
        else:
            if row + 1 == self.height:
                self.current_figure = (None, None)
            elif self.board[row + 1][col]:
                self.current_figure = (None, None)
            else:
                self.move_figure('down')

            if all(self.board[-1]):
                self.board[-1] = [0] * self.width
                self.score += 100

    def render(self, screen):
        screen.fill((0, 0, 0))
        cell_size = self.cell_size
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(screen,
                                 (255, 255, 255),
                                 ((col * cell_size, row * cell_size),
                                  (cell_size, cell_size)),
                                 not bool(self.board[row][col]))


if __name__ == '__main__':
    con = sqlite3.connect('database.sqlite')
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Results (
        nickname STRING PRIMARY KEY,
        score INTEGER
    )""")

    tetris = Tetris(10, 15, 30)
    tetris.add_figure()

    DEFAULT_SPEED = 10
    INCREASED_SPEED = 50

    pygame.init()
    pygame.display.set_caption('Тетрис')
    size = width, height = 300, 450
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 15
    speed = DEFAULT_SPEED
    current_tick = 0
    current_key = None

    running = True
    while running:
        clock.tick(fps)

        current_tick += speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [97, 100, 115]:
                    current_key = event.key
            elif event.type == pygame.KEYUP:
                if event.key in [97, 100, 115]:
                    current_key = None

        if current_key == 97:
            tetris.move_figure('left')
        elif current_key == 100:
            tetris.move_figure('right')
        elif current_key == 115:  # pressed S
            speed = INCREASED_SPEED
        else:
            speed = DEFAULT_SPEED

        if current_tick >= 50:
            tetris.tick()
            current_tick = 0

        tetris.render(screen)
        pygame.display.flip()

    pygame.quit()

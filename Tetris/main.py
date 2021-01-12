from copy import deepcopy
import pygame
import random
import sqlite3


class Figure:
    def __init__(self, tetris, position, blocks):
        self.tetris = tetris
        for idx in range(len(blocks)):
            blocks[idx][0] += position[0]
            blocks[idx][1] += position[1]
            row, col = blocks[idx]
            if tetris.board[row][col] == 1:
                return False
            tetris.board[row][col] = 1
        self.blocks = blocks

    def get_most_down(self):
        return max([row for row, col in self.blocks])

    def get_most_left(self):
        return min([col for row, col in self.blocks])

    def get_most_right(self):
        return max([col for row, col in self.blocks])

    def move_down(self):
        if self.get_most_down() + 1 >= self.tetris.height:
            return False

        blocks = deepcopy(self.blocks)
        board = deepcopy(tetris.board)

        for idx in range(len(blocks)):
            row, col = blocks[idx]
            board[row][col] = 0
            blocks[idx] = (row + 1, col)

        for row, col in blocks:
            if board[row][col] == 1:
                break
            board[row][col] = 1
        else:
            self.blocks = blocks
            tetris.board = board
            return True
        return False

    def move_left(self):
        if self.get_most_down() + 1 >= self.tetris.height or \
           self.get_most_left() <= 0:
            return False

        blocks = deepcopy(self.blocks)
        board = deepcopy(tetris.board)

        for idx in range(len(blocks)):
            row, col = blocks[idx]
            board[row][col] = 0
            blocks[idx] = (row, col - 1)

        for row, col in blocks:
            if board[row][col] == 1:
                break
            board[row][col] = 1
        else:
            self.blocks = blocks
            tetris.board = board
            return True
        return False

    def move_right(self):
        if self.get_most_down() + 1 >= self.tetris.height or \
           self.get_most_right() + 1 >= self.tetris.width:
            return False

        blocks = deepcopy(self.blocks)
        board = deepcopy(tetris.board)

        for idx in range(len(blocks)):
            row, col = blocks[idx]
            board[row][col] = 0
            blocks[idx] = (row, col + 1)

        for row, col in blocks:
            if board[row][col] == 1:
                break
            board[row][col] = 1
        else:
            self.blocks = blocks
            tetris.board = board
            return True
        return False

    def rotate(self, n):
        for i in range(n):
            self.rotate_()

    def rotate_(self):
        x_offset = min([i[0] for i in self.blocks])
        y_offset = min([i[1] for i in self.blocks])

        m = [[0] * 4 for i in range(4)]

        for block in self.blocks:
            tetris.board[block[0]][block[1]] = 0
            m[block[0] - x_offset][block[1] - y_offset] = 1

        for i in range(5, 0, -1):
            m_ = [j[:i] for j in m[:i]]
            if sum(m_, []).count(1) != 4:
                break

        m = [j[:i + 1] for j in m[:i + 1]]
        a = [[m[j][i] for j in range(len(m))] for i in range(len(m[0]) -1, -1, -1)]

        for i in a:
            if not any(i):
                x_offset -= 1
            else:
                break

        for i in range(len(a)):
            if not any([j[i] for j in a]):
                y_offset -= 1
            else:
                break

        new_blocks = []

        for i in range(len(a)):
            for j in range(len(a)):
                if a[i][j] == 1:
                    tetris.board[i + x_offset][j + y_offset] = 1
                    new_blocks.append([i + x_offset, j + y_offset])

        self.blocks = new_blocks

        m = [[0] * 4 for i in range(4)]

        for block in self.blocks:
            m[block[0] - x_offset][block[1] - y_offset] = 1


class Hero(Figure):
    def __init__(self, tetris, position):
        blocks = [
            [0, 0],
            [0, 1],
            [0, 2],
            [0, 3]
        ]
        super().__init__(tetris, position, blocks)


class Smashboy(Figure):
    def __init__(self, tetris, position):
        blocks = [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1]
        ]
        super().__init__(tetris, position, blocks)


class Teewee(Figure):
    def __init__(self, tetris, position):
        blocks = [
            [0, 1],
            [1, 0],
            [1, 1],
            [1, 2]
        ]
        super().__init__(tetris, position, blocks)


class OrangeRicky(Figure):
    def __init__(self, tetris, position):
        blocks = [
            [0, 2],
            [1, 0],
            [1, 1],
            [1, 2]
        ]
        super().__init__(tetris, position, blocks)


class BlueRicky(Figure):
    def __init__(self, tetris, position):
        blocks = [
            [0, 0],
            [1, 0],
            [1, 1],
            [1, 2]
        ]
        super().__init__(tetris, position, blocks)


class Cleveland(Figure):
    def __init__(self, tetris, position):
        blocks = [
            [0, 0],
            [0, 1],
            [1, 1],
            [1, 2]
        ]
        super().__init__(tetris, position, blocks)


class RhodeIsland(Figure):
    def __init__(self, tetris, position):
        blocks = [
            [0, 1],
            [0, 2],
            [1, 0],
            [1, 1]
        ]
        super().__init__(tetris, position, blocks)


class Tetris:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.current_figure = None
        self.cell_size = cell_size
        self.score = 0

    def add_figure(self, figure):
        col = random.randint(3, self.width - 4)
        self.current_figure = figure(self, (0, col))
        if self.current_figure == False:
            exit()  # TODO: Game over!

    def tick(self):
        figure = self.current_figure
        if figure is None:
            self.add_figure(next(FIGURES_SEQUENCE))
        else:
            if figure.get_most_down() == self.height:
                self.current_figure = None
            elif figure.move_down() == False:
                self.current_figure = None

            while all(self.board[-1]):
                self.board = [[0] * self.width] + self.board[:-1]
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


def figures_sequence(figures):
    figures_copy = figures[:]
    while True:
        figure = random.choice(figures_copy)
        figures_copy = figures[:]
        figures_copy.remove(figure)
        yield figure


if __name__ == '__main__':
    DEFAULT_SPEED = 6
    INCREASED_SPEED = 30
    FIGURES = [Hero, Smashboy, Teewee, OrangeRicky,
               BlueRicky, Cleveland, RhodeIsland]
    FIGURES_SEQUENCE = figures_sequence(FIGURES)

    con = sqlite3.connect('database.sqlite')
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Results (
        nickname STRING PRIMARY KEY,
        score INTEGER
    )""")

    tetris = Tetris(10, 15, 30)
    tetris.add_figure(next(FIGURES_SEQUENCE))

    pygame.init()
    pygame.display.set_caption('Тетрис')
    size = width, height = 300, 450
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 15
    speed = DEFAULT_SPEED
    current_tick = 0
    current_key = None
    next_figure = None

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
                elif event.key == 101:
                    tetris.current_figure.rotate(3)
                elif event.key == 113:
                    tetris.current_figure.rotate(1)
            elif event.type == pygame.KEYUP:
                if event.key in [97, 100, 115]:
                    current_key = None

        if tetris.current_figure:
            if current_key == 97:  # pressed A
                tetris.current_figure.move_left()
            elif current_key == 100:  # pressed D
                tetris.current_figure.move_right()
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

import pygame
import sqlite3


class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.current_figure = (None, None)
        self.cell_size = 39

    def tick(self, screen):
        row, col = self.current_figure
        if row is None:
            pass  # TODO: generate new figure
        else:
            if self.board[row + 1][col]:
                self.current_figure = (None, None)
            else:
                self.current_figure = (row + 1, col)
                self.board[row][col] = 0
                self.board[row + 1][col] = 1


if __name__ == '__main__':
    con = sqlite3.connect('database.sqlite')
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Results (
        nickname STRING PRIMARY KEY,
        score INTEGER
    )""")

    board = Tetris(10, 20)

    pygame.init()
    pygame.display.set_caption('Тетрис')
    size = width, height = 390, 780
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # TODO

        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()

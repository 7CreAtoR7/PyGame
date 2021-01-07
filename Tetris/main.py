import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.cell_size = 39

    def on_click(self, x, y):
        pass # TODO

    def render(self, screen):
        pass # TODO


board = Board(10, 20)

pygame.init()
pygame.display.set_caption('Тетрис')
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 10

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

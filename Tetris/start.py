import pygame
import pygame_gui
import os
import sys

class Start:

    def __init__(self, screen, all_sprites):

        run = True

        while run:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == go:
                            pass
                        elif event.ui_element == to_exit:
                            sys.exit()

                manager.process_events(event)
            manager.update(time_delta)
            manager.draw_ui(screen)

            all_sprites.draw(screen)
            pygame.display.update()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    fullname = "C:/Users/xartu/OneDrive/Рабочий стол/Work plase/Pesyah Vs Python/PyGame/Tetris/data/Start_Fon.jpg"
    image = pygame.image.load(fullname)
    return image


pygame.init()
size = weight, height = 1400, 900
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pygame.display.set_caption('Welcome to Tetris')

all_sprites = pygame.sprite.Group()
image = pygame.sprite.Sprite()
image.image = load_image('Start_Fon.jpg')
image.rect = image.image.get_rect()
image.rect.x = 0
image.rect.y = 0
all_sprites.add(image)
all_sprites.draw(screen)



manager = pygame_gui.UIManager((1400, 900))

go = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((510, 110), (450, 350)),
    text='',
    manager=manager
)

to_exit = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((450, 490), (450, 350)),
    text='',
    manager=manager
)


Start(screen, all_sprites)
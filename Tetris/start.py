import pygame
import pygame_gui
import os
import sys

class Start:

    def __init__(self, screen, all_sprites):

        self.name = ''

        run = True

        while run:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == go:
                            if label.text != '':
                                self.name = label.text
                                return

                        elif event.ui_element == to_exit:
                            sys.exit()


                manager.process_events(event)
                manager1.process_events(event)

            manager.update(time_delta)
            manager.draw_ui(screen)

            all_sprites.draw(screen)
            manager1.update(time_delta)
            manager1.draw_ui(screen)
            pygame.display.update()
            pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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
manager1 = pygame_gui.UIManager((1400, 900), 'text_entry_line.json')
#510 110
go = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((450, 350), (500, 100)),
    text='',
    manager=manager,
    visible=1
)
#450 490
to_exit = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((450, 490), (500, 100)),
    text='',
    manager=manager,
    visible=1
)
#300 230
label = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((298, 220), (805, -1)),
    manager=manager1
)

if __name__ == "__main__":
    nickname = Start(screen, all_sprites)
    nickname = nickname.name
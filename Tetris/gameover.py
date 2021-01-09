import os
import sys
import pygame

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1400, 900
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Тетрис')


    def load_image(name):

        # если программа не видит изображение, пропишите полный путь
        # с двумя \\: C:\\Users\\iljal\\PycharmProjects\\main\\data
        fullname = os.path.join('data', name)

        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image


    class Car(pygame.sprite.Sprite):
        image = load_image("game over.jpg")  # это фото game over

        def __init__(self, *group):
            super().__init__(*group)
            self.image = Car.image
            self.rect = self.image.get_rect()
            self.rect.x = -600
            self.rect.y = 212

        def update(self, step):
            if self.rect.x >= 300:
                self.rect.x = 300  # ценрт по иксу
                self.rect.y = 212  # центр по игреку
            else:
                self.rect = self.rect.move(step, 0)


    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("background.jpg")  # это звездный фон
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)

    for _ in range(1):
        Car(all_sprites)

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 255))
        # в главном игровом цикле
        all_sprites.draw(screen)

        clock.tick(500)  # задержка
        all_sprites.update(3)  # При двух - в 2 раза быстрее обычного, при трех - в три и т.д.
        pygame.display.flip()
    pygame.quit()

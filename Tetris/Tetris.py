import pygame
import pygame_gui
import os
import sys
import random
import sqlite3 # в бд заносится никнейм и количество очков игрока
import time
from copy import deepcopy

NAME_LIST = []  # хранится имя игрока


def play_sound(name):
    pygame.mixer.music.load(f'data/{name}.mp3')
    pygame.mixer.music.play()


class Start:
    def __init__(self, screen, all_sprites):
        self.name = ''
        pygame.mixer.music.load('data/music.mp3')  # подключаем музыку
        pygame.mixer.music.play(-1)

        run = True
        while run:
            time_delta = clock.tick(60) / 1000.0 #устанавливаем таймер
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.USEREVENT: #обработка ивентов pygame_gui
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == go:
                            if label.text != '':
                                self.name = label.text
                                NAME_LIST.append(self.name)
                                return

                        elif event.ui_element == to_exit:
                            sys.exit()

                manager.process_events(event)
                manager1.process_events(event)

            manager.update(time_delta) #кнопки рисуются раньше окна
            manager.draw_ui(screen)

            all_sprites.draw(screen) #рисуется фон
            manager1.update(time_delta)
            manager1.draw_ui(screen) #рисуется поле ввода
            pygame.display.update()
            pygame.display.flip()


def load_image(name): # Функция загрузки файла
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
image.image = pygame.image.load('data/Start_Fon.jpg') #Фон для стартового окна
image.rect = image.image.get_rect()
image.rect.x = 0
image.rect.y = 0
all_sprites.add(image)
all_sprites.draw(screen)

manager = pygame_gui.UIManager((1400, 900))
manager1 = pygame_gui.UIManager((1400, 900), 'text_entry_line.json') # Создание 2-ух менеджеров для кнопок и поля отдельно
# 450 350 - положение кнопки "Начать"
go = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((450, 350), (500, 100)),
    text='',
    manager=manager,
    visible=1
)
# 450 490 - положения кнопки "Выйти"
to_exit = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((450, 490), (500, 100)),
    text='',
    manager=manager,
    visible=1
)
# 300 230 - положение поля ввода
label = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((298, 220), (805, -1)),
    manager=manager1
)
# инициализируем игру и стартовое окно
nickname = Start(screen, all_sprites)
nickname = nickname.name


class Figure:
    def __init__(self, tetris, position, blocks, color):
        self.tetris = tetris
        for idx in range(len(blocks)):
            # записываем в self.blocks координаты всех блоков фигуры
            blocks[idx][0] += position[0]
            blocks[idx][1] += position[1]
            row, col = blocks[idx]
            if tetris.board[row][col] == 1:
                return
            tetris.board[row][col] = 1
            tetris.colors[row][col] = color
        self.blocks = blocks
        self.color = color

    def update_result(self):
        # функция обновления результата в таблице лидеров

        nickname = self.tetris.nickname
        score = self.tetris.score

        lb = cur.execute(f"""SELECT * FROM Results WHERE
                             nickname='{nickname}'""").fetchall()

        if not lb:
            cur.execute(f"""INSERT INTO Results VALUES (
                '{nickname}',
                {score})""")
        else:
            cur.execute(f"""UPDATE Results
                SET score={score}
                WHERE nickname='{nickname}'""")

        con.commit()

    def finish_game(self):  # функция обработки финиша игры
        play_sound('gameover')
        pygame.init()
        size = 1400, 900
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Тетрис')

        def load_image(name):  # загружаем изображения фона и надписи game over
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
            Car(all_sprites)  # спрайт Game Over

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

    def get_most_down(self):
        # функция получения самой нижней клетки фигуры

        try:
            return max([row for row, col in self.blocks])
        except:
            self.update_result()
            self.finish_game()
            exit()

    def get_most_left(self):
        # функция получения самой левой клетки фигуры

        try:
            return min([col for row, col in self.blocks])
        except:
            self.update_result()
            self.finish_game()
            exit()

    def get_most_right(self):
        # функция получения самой правой клетки фигуры

        try:
            return max([col for row, col in self.blocks])
        except:
            self.update_result()
            self.finish_game()
            exit()

    def move_down(self):
        # функция перемещения фигуры вниз

        if self.get_most_down() + 1 >= self.tetris.height:
            return False

        # копии
        blocks = deepcopy(self.blocks)
        board = deepcopy(tetris.board)
        colors = deepcopy(tetris.colors)

        for idx in range(len(blocks)):
            row, col = blocks[idx]
            board[row][col] = 0  # опустошаем клетку
            colors[row][col] = 0
            blocks[idx] = (row + 1, col)  # обновляем координаты блока фигуры

        for row, col in blocks:
            if board[row][col] == 1:
                break  # если в новой позиции уже есть занятые клетки, break
            board[row][col] = 1
            colors[row][col] = self.color
        else:
            self.blocks = blocks
            tetris.board = board
            tetris.colors = colors
            return True
        return False

    def move_left(self):
        # функция перемещения фигуры влево

        if self.get_most_left() <= 0:
            return False  # если новые координаты выходят за границы

        # копии
        blocks = deepcopy(self.blocks)
        board = deepcopy(tetris.board)
        colors = deepcopy(tetris.colors)

        for idx in range(len(blocks)):
            row, col = blocks[idx]
            board[row][col] = 0  # опустошаем клетку
            colors[row][col] = 0
            blocks[idx] = (row, col - 1)  # обновляем координаты блока фигуры

        for row, col in blocks:
            if board[row][col] == 1:
                break  # если в новой позиции уже есть занятые клетки, break
            board[row][col] = 1
            colors[row][col] = self.color
        else:
            self.blocks = blocks
            tetris.board = board
            tetris.colors = colors
            return True
        return False

    def move_right(self):
        # функция перемещения фигуры вправо

        if self.get_most_right() + 1 >= self.tetris.width:
            return False  # если новые координаты выходят за границы

        blocks = deepcopy(self.blocks)
        board = deepcopy(tetris.board)
        colors = deepcopy(tetris.colors)

        for idx in range(len(blocks)):
            row, col = blocks[idx]
            board[row][col] = 0  # опустошаем клетку
            colors[row][col] = 0
            blocks[idx] = (row, col + 1)  # обновляем координаты блока фигуры

        for row, col in blocks:
            if board[row][col] == 1:
                break  # если в новой позиции уже есть занятые клетки, break
            board[row][col] = 1
            colors[row][col] = self.color
        else:
            self.blocks = blocks
            tetris.board = board
            tetris.colors = colors
            return True
        return False

    def rotate(self, n):
        # функция поворота фигуры на 90 градусов n раз

        for i in range(n):
            self.rotate_()

        play_sound('rotate')

    def rotate_(self):
        # функция поворота фигуры на 90 градусов

        # смещения координат фигуры относительно (0, 0)
        x_offset = min([i[0] for i in self.blocks])
        y_offset = min([i[1] for i in self.blocks])

        # заготовка для новой фигуры
        m = [[0] * 4 for i in range(4)]

        board = deepcopy(tetris.board)
        colors = deepcopy(tetris.colors)

        for block in self.blocks:
            board[block[0]][block[1]] = 0
            colors[block[0]][block[1]] = 0
            m[block[0] - x_offset][block[1] - y_offset] = 1

        for i in range(5, 0, -1):
            # убираем пустые ряды
            m_ = [j[:i] for j in m[:i]]
            if sum(m_, []).count(1) != 4:
                break

        m = [j[:i + 1] for j in m[:i + 1]]
        a = [[m[j][i] for j in range(len(m))] for \
            i in range(len(m[0]) - 1, -1, -1)]

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
                    board[i + x_offset][j + y_offset] = 1
                    colors[i + x_offset][j + y_offset] = self.color
                    new_blocks.append([i + x_offset, j + y_offset])

        self.blocks = new_blocks

        m = [[0] * 4 for i in range(4)]

        for block in self.blocks:
            m[block[0] - x_offset][block[1] - y_offset] = 1

        tetris.board = board
        tetris.colors = colors


class Hero(Figure):
    def __init__(self, tetris, position, color):
        blocks = [
            [0, 0],
            [0, 1],
            [0, 2],
            [0, 3]
        ]
        super().__init__(tetris, position, blocks, color)


class Smashboy(Figure):
    def __init__(self, tetris, position, color):
        blocks = [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1]
        ]
        super().__init__(tetris, position, blocks, color)


class Teewee(Figure):
    def __init__(self, tetris, position, color):
        blocks = [
            [0, 1],
            [1, 0],
            [1, 1],
            [1, 2]
        ]
        super().__init__(tetris, position, blocks, color)


class OrangeRicky(Figure):
    def __init__(self, tetris, position, color):
        blocks = [
            [0, 2],
            [1, 0],
            [1, 1],
            [1, 2]
        ]
        super().__init__(tetris, position, blocks, color)


class BlueRicky(Figure):
    def __init__(self, tetris, position, color):
        blocks = [
            [0, 0],
            [1, 0],
            [1, 1],
            [1, 2]
        ]
        super().__init__(tetris, position, blocks, color)


class Cleveland(Figure):
    def __init__(self, tetris, position, color):
        blocks = [
            [0, 0],
            [0, 1],
            [1, 1],
            [1, 2]
        ]
        super().__init__(tetris, position, blocks, color)


class RhodeIsland(Figure):
    def __init__(self, tetris, position, color):
        blocks = [
            [0, 1],
            [0, 2],
            [1, 0],
            [1, 1]
        ]
        super().__init__(tetris, position, blocks, color)


class Tetris:
    def __init__(self, width, height, cell_size, x_offset, y_offset, nickname):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.current_figure = None
        self.offset = x_offset, y_offset
        self.cell_size = cell_size
        self.nickname = nickname
        self.score = 0
        self.colors = [[0] * width for _ in range(height)]

    def add_figure(self, figure):
        # метод добавления фигуры на поле

        col = random.randint(3, self.width - 4)
        self.current_figure = figure[0](self, (0, col), figure[1])

    def tick(self):
        # метод обработки одного тика игры

        global next_figure

        figure = self.current_figure
        if figure is None:
            cnt = 0
            board = deepcopy(self.board)
            i = self.height - 1
            while i >= 0:
                # цикл обработки заполненных рядов
                if all(board[i]):
                    board.pop(i)
                    board = [[0] * self.width] + board
                    cnt += 1
                else:
                    i -= 1
            self.board = board

            # выдача очков за ряды
            if 0 < cnt < 5:
                play_sound('complete')

            if cnt == 1:
                self.score += 100
            elif cnt == 2:
                self.score += 300
            elif cnt == 3:
                self.score += 500
            elif cnt == 4:
                self.score += 1000

            self.add_figure(next_figure) # Если на поле нет фигуры, добавляем
            next_figure = next(FIGURES_SEQUENCE)
        else:
            if figure.get_most_down() == self.height: # если фигура в самом низу
                self.current_figure = None
            elif figure.move_down() == False:
                self.current_figure = None

    def render(self, screen):
        # метод для рендеринга поля на экран

        x, y = self.offset
        cs = self.cell_size

        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         ((x, y),
                          (self.width * cs, self.height * cs)),
                         1)

        b_group = pygame.sprite.Group()

        for row in range(self.height):
            for col in range(self.width):
                if bool(self.board[row][col]):
                    im = b_images[self.colors[row][col]]
                    sp = pygame.sprite.Sprite()
                    sp.image = im
                    sp.rect = sp.image.get_rect()
                    sp.rect.x = x + col * cs
                    sp.rect.y = y + row * cs
                    b_group.add(sp)

        b_group.draw(screen)


def figures_sequence(figures, sprites):
    # функция последовательности случайных фигур

    figures_copy = figures[:]
    sprites_copy = sprites[:]

    while True:
        figure = random.choice(figures_copy)
        figures_copy = figures[:]
        figures_copy.remove(figure)

        sprite = random.choice(sprites_copy)
        sprites_copy = sprites[:]
        sprites_copy.remove(sprite)

        yield figure, sprite


if __name__ == '__main__':
    DEFAULT_SPEED = 6
    INCREASED_SPEED = 80
    FIGURES = [Hero, Smashboy, Teewee, OrangeRicky,
               BlueRicky, Cleveland, RhodeIsland]
    # загрузка спрайтов
    b_images = []
    for i in range(1, 8):
        im = pygame.image.load(f'data/Block{i}.png')
        b_images.append(im)

    FIGURES_SEQUENCE = figures_sequence(FIGURES, [i for i in range(7)])

    con = sqlite3.connect('database.sqlite')
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Results (
        nickname STRING PRIMARY KEY,
        score INTEGER
    )""")

    tetris = Tetris(10, 20, 39, 601, 55, str(NAME_LIST[0]))

    bg = pygame.image.load('data/Game_Form.png')

    tetris.add_figure(next(FIGURES_SEQUENCE))
    next_figure = next(FIGURES_SEQUENCE)

    pygame.init()
    pygame.display.set_caption('Тетрис')
    size = width, height = 1400, 900
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 15
    speed = DEFAULT_SPEED
    current_tick = 0
    current_key = None
    font = pygame.font.SysFont(None, 60)
    font2 = pygame.font.SysFont(None, 30)

    start_time = time.time()

    manager2 = pygame_gui.UIManager((1400, 900))

    pause = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((1200, 250), (180, 100)),
        text='',
        manager=manager2
    )
    # 450 490
    to_exit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((1200, 775), (180, 100)),
        text='',
        manager=manager2
    )

    pygame.mixer.music.unload()

    running = True
    paused = False
    while running:
        clock.tick(fps)

        current_tick += speed

        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and not paused:
                if event.key in [97, 100, 115]:
                    current_key = event.key
                elif event.key == 101:
                    try:
                        tetris.current_figure.rotate(3)
                    except:
                        pass
                elif event.key == 113:
                    try:
                        tetris.current_figure.rotate(1)
                    except:
                        pass

            elif event.type == pygame.KEYUP and not paused:
                if event.key in [97, 100, 115]:
                    current_key = None

            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == pause:
                        play_sound('pause')
                        paused = not paused
                        if paused:
                            pause_time = time.time()
                        else:
                            start_time += time.time() - pause_time

                    elif event.ui_element == to_exit:
                        sys.exit()

            manager2.process_events(event)

        if tetris.current_figure and not paused:
            if current_key == 97:  # pressed A
                try:
                    tetris.current_figure.move_left()
                except:
                    pass
            elif current_key == 100:  # pressed D
                try:
                    tetris.current_figure.move_right()
                except:
                    pass
            elif current_key == 115:  # pressed S
                speed = INCREASED_SPEED
            else:
                speed = DEFAULT_SPEED

        if current_tick >= 50 and not paused:
            tetris.tick()
            current_tick = 0

        manager2.update(time_delta)
        manager2.draw_ui(screen)

        tetris.render(screen)

        if paused:
            timer = int(pause_time - start_time)
        else:
            timer = int(time.time() - start_time)
        m, s = str(timer // 60), str(timer % 60)
        if len(s) == 1:
            s = '0' + s

        text = font.render(f'{m}:{s}', False, (255, 200, 123))
        screen.blit(text, (1250, 165))

        text = font.render(f'{tetris.score}', False, (255, 200, 123))
        screen.blit(text, (1275, 45))

        leaders = cur.execute(f"""SELECT score, nickname FROM Results WHERE 1""").fetchall()
        leaders = sorted(leaders, reverse=True)
        tx = [f'{i + 1}. {leaders[i][1]}: {leaders[i][0]}' for i in range(len(leaders))]

        text = font2.render('Таблица лидеров:', False, (0, 255, 0))
        screen.blit(text, (100, 270))

        for t in range(len(tx)):
            text = font2.render(tx[t], False, (0, 255, 0))
            screen.blit(text, (100, 320 + t * 40))

        pygame.display.flip()

    pygame.quit()

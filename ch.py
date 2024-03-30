import pygame
import random
import pygame_menu
import pygame.mixer

import subprocess

import os


# инициализация pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('lose_sound.mp3')

# цвета
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
more_color = (66, 133, 180)
zel = (155, 188, 15)

# инициализация pygame
pygame.display.set_caption('Хорз змейка')
sc = pygame.display.set_mode((400, 300))
sc.fill(red)

score_texxt = []


def start_the_game():
    # начало игры
    # в зависимости от режима вызываются разные функции
    if rezim.get_value()[1] == 0:
        first_level()
    elif rezim.get_value()[1] == 1:
        second_level()
    else:
        thirth_level()


def first_level():
    lev = '1'
    window_x = 672
    window_y = 672
    snake_speed = 5
    os.environ['SDL_VIDEO_WINDOW_POS'] = '1'
    game_window = pygame.display.set_mode((window_x, window_y))

    # FPS контроллер
    fps = pygame.time.Clock()
    snake_razmre = 32
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    apple_sprite = pygame.sprite.Sprite()
    # определим его вид
    sprite.image = pygame.image.load('green_snake.png').convert_alpha()
    # apple_sprite.image = pygame.image.load('apple_alt_32.png').convert_alpha()
    snake_position = [50, 50]
    # и размеры
    sprite.rect = sprite.image.get_rect(center=(snake_position[0], snake_position[1]))
    # добавим спрайт в группу
    all_sprites.add(sprite)

    # тело змейки
    # изначально первый блок
    snake_body = [[0, 0]]
    # позиция яблока
    fruit_spawn = True
    while fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // snake_razmre)) * snake_razmre,
                          random.randrange(1, (window_y // snake_razmre)) * snake_razmre]

        # Проверяем, не совпадает ли позиция яблока с позицией змейки
        while fruit_position in snake_body:
            fruit_position = [random.randrange(1, (window_x // snake_razmre)) * snake_razmre,
                              random.randrange(1, (window_y // snake_razmre)) * snake_razmre]

        # Создаем спрайт для яблока
        apple_sprite = pygame.sprite.Sprite()
        apple_sprite.image = pygame.image.load('apple_alt_32.png').convert_alpha()
        apple_sprite.rect = apple_sprite.image.get_rect(center=(fruit_position[0], fruit_position[1]))
        all_sprites.add(apple_sprite)
        fruit_spawn = False

    # direction - направление змейки
    # change_to - направление кнопки
    # изначально RIGHT т к ещё не нажата кнопка
    direction = 'RIGHT'
    change_to = direction

    # score - подсчет очков
    score = 10
    game = True
    while game:
        game_window.fill(white)
        # проверка на нажатие кнопок клавиатуры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over(game_window, score, lev)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # далее проверка на то, что не нажаты противоположные кнопки
        # если змейка напрявлялась вправо, а игрок нажал влево, то нажатие игнорируется
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # движение змейки
        change_xy = 10
        if direction == 'UP':
            sprite.rect.y -= snake_razmre
            snake_position[1] -= snake_razmre
            sprite.image = pygame.image.load('green_snake.png').convert_alpha()
        if direction == 'DOWN':
            sprite.rect.y += snake_razmre
            snake_position[1] += snake_razmre
            sprite.image = pygame.image.load('down_snake.png').convert_alpha()
        if direction == 'LEFT':
            sprite.rect.x -= snake_razmre
            snake_position[0] -= snake_razmre
            sprite.image = pygame.image.load('left_snake.png').convert_alpha()
        if direction == 'RIGHT':
            sprite.rect.x += snake_razmre
            snake_position[0] += snake_razmre
            sprite.image = pygame.image.load('right_snake.png').convert_alpha()

        # в Snake body добавляются части змейки
        # проверка на столкновение с яблоком
        # при столкновении прибавляется 10 очков и меняется позиция фрукта
        snake_body.insert(0, list(snake_position))
        if sprite.rect.colliderect(apple_sprite.rect):
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // snake_razmre)) * snake_razmre,
                              random.randrange(1, (window_y // snake_razmre)) * snake_razmre]
            apple_sprite.rect.x = fruit_position[0]
            apple_sprite.rect.y = fruit_position[1]

        fruit_spawn = True
        game_window.fill(more_color)
        all_snake = pygame.sprite.Group()

        # отрисовка змейки
        for pos in snake_body[1:]:
            kus = pygame.sprite.Sprite()
            kus.image = pygame.image.load('snake_blue.png').convert_alpha()
            kus.rect = sprite.image.get_rect(center=(pos[0], pos[1]))
            all_snake.add(kus)

        # отрисовка фрукта

        # если змейка врезалась в стекну, то она появляется с другой стороны
        if sprite.rect.x <= 0:
            game_lose(game_window, score, lev)
        if sprite.rect.x >= window_x:
            game_lose(game_window, score, lev)
        if sprite.rect.y <= 0:
            game_lose(game_window, score, lev)
        if sprite.rect.y >= window_y:
            game_lose(game_window, score, lev)

        # проверка на столкновение с собой
        for i in all_snake:
            if sprite.rect.colliderect(i.rect):
                game_lose(game_window, score, lev)

        # отображение очков в верхнем правом углу
        show_score(game_window, white, 'times new roman', 20, score)

        # обновление экрана
        all_snake.draw(game_window)
        all_sprites.draw(game_window)
        pygame.display.update()

        # скорость обновления экрана
        fps.tick(snake_speed)


mina_pozition = []
window_x = 720
window_y = 480
snake_razmre = 15


def game_over(game_window, score, lev):
    text_for_list = str(f'Игрок {usernam.get_value()} заработал {score} на {lev} уровне \n')
    score_texxt.append(text_for_list)
    with open('score_list.txt', 'a', encoding='utf-8') as f:
        f.writelines(score_texxt)
        f.close()
    pygame.quit()
    quit()


def show_score(game_window, color, font, size, score):
    # отображение скорости
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)


def game_lose(game_window, score, lev):
    pygame.mixer.music.play()
    # текст для сохранения в файл с именем играка и количеством очков
    text_for_list = str(f'Игрок {usernam.get_value()} заработал {score} на {lev} уровне \n')
    score_texxt.append(text_for_list)
    with open('score_list.txt', 'a', encoding='utf-8') as f:
        f.writelines(score_texxt)
        f.close()
    # меню проигрыша
    lose_text = 'Ты проиграл, твой счет ' + str(score)
    lose_mennu = pygame_menu.Menu(lose_text, 400, 300,
                                  theme=pygame_menu.themes.THEME_BLUE)
    lose_mennu.add.button('Начать сначала', start_the_game)
    lose_mennu.add.button('Покинуть игру', pygame_menu.events.EXIT)

    lose_mennu.mainloop(game_window)




def second_level():
    snake_speed = 5
    lev = '2'
    her_w = 32
    window_x = 672
    window_y = 672
    game_window = pygame.display.set_mode((window_x, window_y))

    # FPS контроллер
    fps = pygame.time.Clock()
    snake_razmre = 32
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    apple_sprite = pygame.sprite.Sprite()
    # определим его вид
    sprite.image = pygame.image.load('green_snake.png').convert_alpha()
    snake_position = [50, 50]
    # и размеры
    sprite.rect = sprite.image.get_rect(center=(snake_position[0], snake_position[1]))
    # добавим спрайт в группу
    all_sprites.add(sprite)

    # тело змейки
    # изначально первый блок
    snake_body = [[0, 0]
                  ]
    stena_poz = 280
    stena = pygame.sprite.Sprite()
    stena.image = pygame.image.load('kamen.png').convert_alpha()
    stena.rect = sprite.image.get_rect(topleft=(stena_poz, stena_poz))
    all_sprites.add(stena)

    stena2_poz = 380
    stena2 = pygame.sprite.Sprite()
    stena2.image = pygame.image.load('stena2.png').convert_alpha()
    stena2.rect = sprite.image.get_rect(topleft=(stena2_poz, stena2_poz))
    all_sprites.add(stena2)
    # позиция яблока
    fruit_spawn = True
    while fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // snake_razmre)) * snake_razmre,
                          random.randrange(1, (window_y // snake_razmre)) * snake_razmre]

        # Проверяем, не совпадает ли позиция яблока с позицией змейки
        while fruit_position in snake_body:
            fruit_position = [random.randrange(1, (window_x // snake_razmre)) * snake_razmre,
                              random.randrange(1, (window_y // snake_razmre)) * snake_razmre]

        # Создаем спрайт для яблока
        apple_sprite = pygame.sprite.Sprite()
        apple_sprite.image = pygame.image.load('apple_alt_32.png').convert_alpha()
        apple_sprite.rect = apple_sprite.image.get_rect(center=(fruit_position[0], fruit_position[1]))
        while apple_sprite.rect.colliderect(stena.rect) or apple_sprite.rect.colliderect(stena2.rect):
            fruit_position = [random.randrange(1, (window_x // snake_razmre)) * snake_razmre,
                              random.randrange(1, (window_y // snake_razmre)) * snake_razmre]

        apple_sprite.rect = apple_sprite.image.get_rect(center=(fruit_position[0], fruit_position[1]))
        all_sprites.add(apple_sprite)
        fruit_spawn = False

    # direction - направление змейки
    # change_to - направление кнопки
    # изначально RIGHT т к ещё не нажата кнопка
    direction = 'RIGHT'
    change_to = direction

    # score - подсчет очков
    score = 10
    game = True
    while game:
        game_window.fill(white)
        # проверка на нажатие кнопок клавиатуры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over(game_window, score, lev)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # далее проверка на то, что не нажаты противоположные кнопки
        # если змейка напрявлялась вправо, а игрок нажал влево, то нажатие игнорируется
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # движение змейки
        change_xy = 10
        if direction == 'UP':
            sprite.rect.y -= snake_razmre
            snake_position[1] -= snake_razmre
            sprite.image = pygame.image.load('green_snake.png').convert_alpha()
        if direction == 'DOWN':
            sprite.rect.y += snake_razmre
            snake_position[1] += snake_razmre
            sprite.image = pygame.image.load('down_snake.png').convert_alpha()
        if direction == 'LEFT':
            sprite.rect.x -= snake_razmre
            snake_position[0] -= snake_razmre
            sprite.image = pygame.image.load('left_snake.png').convert_alpha()
        if direction == 'RIGHT':
            sprite.rect.x += snake_razmre
            snake_position[0] += snake_razmre
            sprite.image = pygame.image.load('right_snake.png').convert_alpha()

        # в Snake body добавляются части змейки
        # проверка на столкновение с яблоком
        # при столкновении прибавляется 10 очков и меняется позиция фрукта
        snake_body.insert(0, list(snake_position))
        if sprite.rect.colliderect(apple_sprite.rect):
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // snake_razmre)) * snake_razmre,
                              random.randrange(1, (window_y // snake_razmre)) * snake_razmre]
            apple_sprite.rect.x = fruit_position[0]
            apple_sprite.rect.y = fruit_position[1]

        fruit_spawn = True
        game_window.fill(more_color)
        all_snake = pygame.sprite.Group()

        # отрисовка змейки
        for pos in snake_body[1:]:
            chast = pygame.sprite.Sprite()
            chast.image = pygame.image.load('snake_blue.png').convert_alpha()
            chast.rect = sprite.image.get_rect(center=(pos[0], pos[1]))
            all_snake.add(chast)

        # отрисовка фрукта

        # если змейка врезалась в стекну, то она появляется с другой стороны
        if sprite.rect.x <= 0:
            game_lose(game_window, score, lev)
        if sprite.rect.x >= window_x:
            game_lose(game_window, score, lev)
        if sprite.rect.y <= 0:
            game_lose(game_window, score, lev)
        if sprite.rect.y >= window_y:
            game_lose(game_window, score, lev)

        # проверка на столкновение с собой
        for i in all_snake:
            if sprite.rect.colliderect(i.rect) or sprite.rect.colliderect(stena.rect):
                game_lose(game_window, score, lev)
        kamen_sten_rect = pygame.draw.rect(game_window, red, (280, 280, 32, 125))
        sten2_rect = pygame.draw.rect(game_window, red, (380, 380, 32, 125))
        if sprite.rect.colliderect(kamen_sten_rect) or sprite.rect.colliderect(sten2_rect):
            game_lose(game_window, score, lev)

        # отображение очков в верхнем правом углу
        show_score(game_window, white, 'times new roman', 20, score)

        # обновление экрана
        all_snake.draw(game_window)
        all_sprites.draw(game_window)

        pygame.display.update()

        # скорость обновления экрана
        fps.tick(snake_speed)


def print_score():
    subprocess.Popen(['notepad', 'score_list.txt'])


def thirth_level():
    new_window_x = 672
    new_window_y = 672
    lev = '1'
    snake_speed = 20
    game_window = pygame.display.set_mode((new_window_x, new_window_y))
    # FPS контроллер
    fps = pygame.time.Clock()
    snake_razmre = 32
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    apple_sprite = pygame.sprite.Sprite()
    # определим его вид
    sprite.image = pygame.image.load('green_snake.png').convert_alpha()
    # apple_sprite.image = pygame.image.load('apple_alt_32.png').convert_alpha()
    snake_position = [50, 50]
    # и размеры
    sprite.rect = sprite.image.get_rect(center=(snake_position[0], snake_position[1]))
    # добавим спрайт в группу
    all_sprites.add(sprite)

    # тело змейки
    # изначально первый блок
    snake_body = [[0, 0]]
    # позиция яблока
    fruit_spawn = True
    while fruit_spawn:
        fruit_position = [random.randrange(1, (new_window_x // snake_razmre)) * snake_razmre,
                          random.randrange(1, (new_window_y // snake_razmre)) * snake_razmre]


        # Проверяем, не совпадает ли позиция яблока с позицией змейки
        while fruit_position in snake_body:
            fruit_position = [random.randrange(1, (new_window_x // snake_razmre)) * snake_razmre,
                              random.randrange(1, (new_window_y // snake_razmre)) * snake_razmre]

        # Создаем спрайт для яблока
        apple_sprite = pygame.sprite.Sprite()
        apple_sprite.image = pygame.image.load('apple_alt_32.png').convert_alpha()
        apple_sprite.rect = apple_sprite.image.get_rect(center=(fruit_position[0], fruit_position[1]))
        all_sprites.add(apple_sprite)
        fruit_spawn = False

    sunduk_spawn = True
    while sunduk_spawn:
        sunduk_pos = [random.randrange(1, (new_window_x // snake_razmre)) * snake_razmre,
                      random.randrange(1, (new_window_y // snake_razmre)) * snake_razmre]

        while sunduk_pos in snake_body or sunduk_pos in fruit_position:
            sunduk_pos = [random.randrange(1, (new_window_x // snake_razmre)) * snake_razmre,
                              random.randrange(1, (new_window_y // snake_razmre)) * snake_razmre]

        sunduk = pygame.sprite.Sprite()
        sunduk.image = pygame.image.load('sun-new.png').convert_alpha()
        sunduk.rect = apple_sprite.image.get_rect(center=(sunduk_pos[0], sunduk_pos[1]))
        all_sprites.add(sunduk)
        sunduk_spawn = False

    # direction - направление змейки
    # change_to - направление кнопки
    # изначально RIGHT т к ещё не нажата кнопка
    direction = 'RIGHT'
    change_to = direction

    # score - подсчет очков
    score = 10
    game = True
    while game:
        game_window.fill(white)
        # проверка на нажатие кнопок клавиатуры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over(game_window, score, lev)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # далее проверка на то, что не нажаты противоположные кнопки
        # если змейка напрявлялась вправо, а игрок нажал влево, то нажатие игнорируется
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # движение змейки
        change_xy = 10
        if direction == 'UP':
            sprite.rect.y -= snake_razmre
            snake_position[1] -= snake_razmre
            sprite.image = pygame.image.load('green_snake.png').convert_alpha()
        if direction == 'DOWN':
            sprite.rect.y += snake_razmre
            snake_position[1] += snake_razmre
            sprite.image = pygame.image.load('down_snake.png').convert_alpha()
        if direction == 'LEFT':
            sprite.rect.x -= snake_razmre
            snake_position[0] -= snake_razmre
            sprite.image = pygame.image.load('left_snake.png').convert_alpha()
        if direction == 'RIGHT':
            sprite.rect.x += snake_razmre
            snake_position[0] += snake_razmre
            sprite.image = pygame.image.load('right_snake.png').convert_alpha()

        # в Snake body добавляются части змейки
        # проверка на столкновение с яблоком
        # при столкновении прибавляется 10 очков и меняется позиция фрукта
        snake_body.insert(0, list(snake_position))
        if sprite.rect.colliderect(apple_sprite.rect):
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (new_window_x // snake_razmre)) * snake_razmre,
                              random.randrange(1, (new_window_y // snake_razmre)) * snake_razmre]
            apple_sprite.rect.x = fruit_position[0]
            apple_sprite.rect.y = fruit_position[1]

        fruit_spawn = True
        game_window.fill(more_color)
        all_snake = pygame.sprite.Group()

        # отрисовка змейки
        for pos in snake_body[1:]:
            kus = pygame.sprite.Sprite()
            kus.image = pygame.image.load('snake_blue.png').convert_alpha()
            kus.rect = sprite.image.get_rect(center=(pos[0], pos[1]))
            all_snake.add(kus)

        # отрисовка фрукта

        # если змейка врезалась в стекну, то она появляется с другой стороны
        if sprite.rect.x <= 0:
            game_lose(game_window, score, lev)
        if sprite.rect.x >= new_window_x:
            game_lose(game_window, score, lev)
        if sprite.rect.y <= 0:
            game_lose(game_window, score, lev)
        if sprite.rect.y >= new_window_y:
            game_lose(game_window, score, lev)

        # проверка на столкновение с собой
        for i in all_snake:
            if sprite.rect.colliderect(i.rect):
                game_lose(game_window, score, lev)

        if sprite.rect.colliderect(sunduk.rect):
            score += 30
            sunduk_spawn = False

        if not sunduk_spawn:
            sunduk_pos = [random.randrange(1, (new_window_x // snake_razmre)) * snake_razmre,
                              random.randrange(1, (new_window_y // snake_razmre)) * snake_razmre]
            sunduk.rect.x = sunduk_pos[0]
            sunduk.rect.y = sunduk_pos[1]

        sunduk_spawn = True

        # отображение очков в верхнем правом углу
        show_score(game_window, white, 'times new roman', 20, score)

        # обновление экрана
        all_snake.draw(game_window)
        all_sprites.draw(game_window)
        pygame.display.update()

        # скорость обновления экрана
        fps.tick(snake_speed)


# начальное меню
menu = pygame_menu.Menu('Меню', 400, 300,
                        theme=pygame_menu.themes.THEME_GREEN)
# ввод имени игрока
usernam = menu.add.text_input('Имя :', default='Player', textinput_id='username')
# выбор режима игры
rezim = menu.add.selector('Уровень : ', [('Первый', 1), ('Второй', 2), ('Третий', 3)])
menu.add.button('Старт', start_the_game)
menu.add.button('Результаты', print_score)
menu.add.button('Выход', pygame_menu.events.EXIT)

# отображение меню
menu.mainloop(sc)

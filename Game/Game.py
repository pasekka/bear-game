# Импорт библиотек
import pygame
import sys
import random
clock = pygame.time.Clock()
pygame.init()

# Настройка экрана
screen = pygame.display.set_mode((810, 1000))
pygame.display.set_caption("Game")

# Загрузка музыки
pygame.mixer.init()
pygame.mixer.music.load("game/audio/bg_music.mp3")
pygame.mixer.music.play(-1)

# Загрузка звуковых эффектов
shot = pygame.mixer.Sound("game/audio/shot.ogg")
reloading = pygame.mixer.Sound("game/audio/reloading.ogg")

# Задать фон
background_y = 0
background = pygame.image.load("game/sprites/assets/back.png").convert()

# Установка шрифта
label = pygame.font.Font("game/fonts/Gagalin-Regular.otf", 40)

# Текст
gameover_text = label.render("Game over!", False, (160,170,185))
again_text = label.render("Again", False, (255,255,255))
again_text_rect = again_text.get_rect(topleft =(355,380))
win_text = label.render("You win", False, (160,170,185))

# Массивы с кадрами анимаций
move_down = [
    pygame.image.load("game/sprites/movement_down/bear1.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_down/bear2.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_down/bear3.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_down/bear4.png").convert_alpha(),    
]
move_back = [
    pygame.image.load("game/sprites/movement_down/bear1.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_down/bear1.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_down/bear1.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_down/bear1.png").convert_alpha(),    
] # Небольшой костыль, чтобы обработчик анимаций не выдавал ошибки стояние на месте указано в 4 одинаковых кадрах.
move_left = [
    pygame.image.load("game/sprites/movement_left/bearL1.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_left/bearL2.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_left/bearL3.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_left/bearL4.png").convert_alpha(),    
]
move_right = [
    pygame.image.load("game/sprites/movement_right/bearR1.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_right/bearR2.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_right/bearR3.png").convert_alpha(),
    pygame.image.load("game/sprites/movement_right/bearR4.png").convert_alpha(),    
]

# Препятствие
obstacle = pygame.image.load("game/sprites/assets/bush1.png").convert_alpha()
obstacles = []
time_to_spawn = 500
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, time_to_spawn)
chosen_sprite = 0

# Подбираемый объект
ammo = pygame.image.load("game/sprites/assets/crate.png").convert_alpha()
ammo_boxes = []
ammo_spawn = 5000
ammo_timer = pygame.USEREVENT + 2
pygame.time.set_timer(ammo_timer, ammo_spawn)

# Противник
bee = [
    pygame.image.load("game/sprites/assets/bee/bee1.png").convert_alpha(),
    pygame.image.load("game/sprites/assets/bee/bee2.png").convert_alpha(),
    pygame.image.load("game/sprites/assets/bee/bee3.png").convert_alpha(),
    pygame.image.load("game/sprites/assets/bee/bee4.png").convert_alpha(),
]
bees = []
bee_spawn = 1000
bee_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bee_timer, bee_spawn)
bees_amount = 0

# Счетчики для кадров анимаций
bear_frame = 0
bee_frame = 0
last_update = 0  # Последнее обновление кадра анимации

# Скорость и координаты 
side_speed = 14
backward_move_speed = 4 
forward_move_speed = 8
bear_x = 380
bear_y = 300

# Пули
projectile = pygame.image.load("game/sprites/assets/projectile.png").convert_alpha()
projectiles = []
projectiles_amount = 3

# Сложность 
level_speed = 2
spawn_speed = 2000
difficulty_timer = pygame.USEREVENT + 4
pygame.time.set_timer(difficulty_timer, 10000)

# Цикл обработки геймплея
run = True
win = False
alive = True

while run:
    interval = 100  # Нужно для правильного отображения анимаций
    clock.tick(30)
    bear_hitbox = move_down[0].get_rect(topleft=(bear_x, bear_y)) # Создание хитбокса персонажа
    mouse = pygame.mouse.get_pos()    

    # Отрисовываем задний фон
    screen.blit(background,(0,background_y))
    screen.blit(background,(0,background_y + 1000))

    if alive:
        # Запускаем музыку заново, если игрок перезапустил игру
        pygame.mixer.music.unpause()
        
        # Генерируем препятствия
        if obstacles:
            for (i, el) in enumerate (obstacles):
                screen.blit(obstacle, el)
                el.y -= level_speed
                if el.y <= -140:
                    obstacles.pop(i)
                if bear_hitbox.colliderect(el):
                    alive = False
        
        # Генерируем противников
        if bees:
            for (i, el) in enumerate (bees):
                screen.blit(bee[bee_frame], el)
                el.y -= level_speed
                if el.y <= -140:
                    bees.pop(i)
                if bear_hitbox.colliderect(el):
                    alive = False
                    
        # Генерируем подбираемые предметы
        if ammo_boxes:
            for (i, el) in enumerate (ammo_boxes):
                screen.blit(ammo, el)
                el.y -= level_speed
                if el.y <= -140:
                    ammo_boxes.pop(i)
                if bear_hitbox.colliderect(el):
                    projectiles_amount += 3    
                    ammo_boxes.pop(i)
                    reloading.play()

        # Обработчик анимации, поочерёдно переключает изображения в массиве с элемента 0 до элемента 3, создавая тем самым анимированного персонажа без прямой привязки к тикам игры.
        if bear_frame == 3:
            bear_frame = 0
            bee_frame = 0 # Это небольшая оптимизация кода, поскольку у обоих персонажей одинаковое количество кадров анимации они обрабатываются по одному и тому же принципу
        elif pygame.time.get_ticks() - last_update > interval: # Проверяка интервала, чтобы анимация персонажа шла не с той же скорость что clock.tick 
            bear_frame += 1
            bee_frame += 1
            last_update = pygame.time.get_ticks()
            
        # Передвижение фона, создавает иллюзию перемещения.
        background_y -= level_speed
        if background_y <= -1000:
            background_y = 0

        # Сделаем управление стрелками. Отдельные команды для передвижения наискосок
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            screen.blit(move_left[bear_frame], (bear_x, bear_y))
            if bear_x >= 15:
                bear_x -= side_speed
            if bear_y >= 0:
                bear_y -= backward_move_speed
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            screen.blit(move_left[bear_frame], (bear_x, bear_y))
            if bear_x >= 15:
                bear_x -= side_speed
            if bear_y <= 890:
                bear_y += forward_move_speed
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            screen.blit(move_right[bear_frame], (bear_x, bear_y))
            if bear_x <= 679:
                bear_x += side_speed
            if bear_y >= 0:
                bear_y -= backward_move_speed
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            screen.blit(move_right[bear_frame], (bear_x, bear_y))
            if bear_x <= 679:
                bear_x += side_speed
            if bear_y <= 890:
                bear_y += forward_move_speed

        # Отдельные команды для передвижения по прямой
        elif keys[pygame.K_LEFT] and bear_x >= 15:
            bear_x -= side_speed
            screen.blit(move_left[bear_frame], (bear_x, bear_y))
        elif keys[pygame.K_RIGHT] and bear_x <= 679:
            bear_x += side_speed
            screen.blit(move_right[bear_frame], (bear_x, bear_y))
        elif keys[pygame.K_UP] and bear_y >= 0:
            bear_y -= backward_move_speed
            screen.blit(move_back[bear_frame], (bear_x, bear_y))
        elif keys[pygame.K_DOWN] and bear_y <= 890:
            bear_y += forward_move_speed
            screen.blit(move_down[bear_frame], (bear_x, bear_y))
        else:
            screen.blit(move_down[bear_frame], (bear_x, bear_y))
            
        # Стрельба
        if projectiles:
            for (i, el) in enumerate (projectiles):
                screen.blit(projectile, (el.x, el.y))
                el.y += 30
                if el.y >= 1020:
                    projectiles.pop(i)
                if bees:
                    for (index, bee_el) in enumerate(bees):
                        if el.colliderect(bee_el):
                            bees.pop(index)
                            projectiles.pop(i)
                            bees_amount += 1
        
        if bees_amount >= 10:
            win = True
            alive = False

        # Отрисовка интерфейса игрока 
        ammo_text = label.render(f"Shots left: {projectiles_amount}", True, (255,255,255))
        screen.blit(ammo_text, (10,10))

        ammo_text = label.render(f"Bees killed: {bees_amount}/10", True, (255,255,255))
        screen.blit(ammo_text, (265,930))

    # Перезагружает игру при поражении
    elif bees_amount < 10:
        screen.fill((69, 124, 155))
        screen.blit(gameover_text,(315, 280))
        screen.blit(again_text, again_text_rect)
        pygame.mixer.music.pause()
        pygame.mixer.music.rewind() # Нужно для того чтобы муызка не продолжалась с того места на котором остановилась в момент поражения
        if again_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            bear_x = 380
            bear_y = 300           
            projectiles_amount = 3
            bees_amount = 0
            obstacles.clear()
            ammo_boxes.clear()
            bees.clear()
            projectiles.clear()
            level_speed = 2
            spawn_speed = 2000
            alive = True

    # Перезагружает игру при победе
    elif bees_amount >= 10: 
        screen.fill((69, 124, 155))
        screen.blit(win_text,(338, 280))
        screen.blit(again_text, again_text_rect)
        pygame.mixer.music.pause()
        pygame.mixer.music.rewind # Нужно для того чтобы муызка не продолжалась с того места на котором остановилась в момент поражения
        if again_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            bear_x = 380
            bear_y = 300           
            projectiles_amount = 3
            bees_amount = 0
            obstacles.clear()
            ammo_boxes.clear()
            bees.clear()
            projectiles.clear()
            level_speed = 2
            spawn_speed = 2000
            alive = True

    pygame.display.update()

    # Обработчик нажатий клавиш и событий
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        # Генерация кустов
        if i.type == obstacle_timer:
            obstacles.append(obstacle.get_rect(topleft=(random.randint(0,810), 1000)))
            pygame.time.set_timer(obstacle_timer, time_to_spawn) 
            time_to_spawn = random.randint(spawn_speed,spawn_speed*2)
        # Генерация патронов
        if i.type == ammo_timer:
            ammo_boxes.append(ammo.get_rect(topleft=(random.randint(0,810),1000)))
            pygame.time.set_timer(ammo_timer, ammo_spawn)
            ammo_spawn = random.randint(5000,15000)
        # Генерация противников
        if i.type == bee_timer:
            bees.append(bee[0].get_rect(topleft=(random.randint(0,810),1000)))
            pygame.time.set_timer(bee_timer, bee_spawn)
            bee_spawn = random.randint(spawn_speed*2,spawn_speed*4)
        # Сложность игры постепенно нарастает чтобы было интереснее    
        if i.type == difficulty_timer:
            if level_speed <= 10:
                level_speed += 1
                spawn_speed -= 200
        # Создание снарядов при выстреле
        if alive and i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE and projectiles_amount > 0:
            projectiles.append(projectile.get_rect(topleft = (bear_x+44, bear_y+65)))
            projectiles_amount -= 1
            shot.play()

pygame.quit()
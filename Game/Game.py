# ������ ���������
import pygame
import sys
import random
clock = pygame.time.Clock()
pygame.init()

# ��������� ������
screen = pygame.display.set_mode((810, 1000))
pygame.display.set_caption("Game")

# �������� ������
pygame.mixer.init()
pygame.mixer.music.load("game/audio/bg_music.mp3")
pygame.mixer.music.play(-1)

# �������� �������� ��������
shot = pygame.mixer.Sound("game/audio/shot.ogg")
reloading = pygame.mixer.Sound("game/audio/reloading.ogg")

# ������ ���
background_y = 0
background = pygame.image.load("game/sprites/assets/back.png").convert()

# ��������� ������
label = pygame.font.Font("game/fonts/Gagalin-Regular.otf", 40)

# �����
gameover_text = label.render("Game over!", False, (160,170,185))
again_text = label.render("Again", False, (255,255,255))
again_text_rect = again_text.get_rect(topleft =(355,380))
win_text = label.render("You win", False, (160,170,185))

# ������� � ������� ��������
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
] # ��������� �������, ����� ���������� �������� �� ������� ������ ������� �� ����� ������� � 4 ���������� ������.
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

# �����������
obstacle = pygame.image.load("game/sprites/assets/bush1.png").convert_alpha()
obstacles = []
time_to_spawn = 500
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, time_to_spawn)
chosen_sprite = 0

# ����������� ������
ammo = pygame.image.load("game/sprites/assets/crate.png").convert_alpha()
ammo_boxes = []
ammo_spawn = 5000
ammo_timer = pygame.USEREVENT + 2
pygame.time.set_timer(ammo_timer, ammo_spawn)

# ���������
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

# �������� ��� ������ ��������
bear_frame = 0
bee_frame = 0
last_update = 0  # ��������� ���������� ����� ��������

# �������� � ���������� 
side_speed = 14
backward_move_speed = 4 
forward_move_speed = 8
bear_x = 380
bear_y = 300

# ����
projectile = pygame.image.load("game/sprites/assets/projectile.png").convert_alpha()
projectiles = []
projectiles_amount = 3

# ��������� 
level_speed = 2
spawn_speed = 2000
difficulty_timer = pygame.USEREVENT + 4
pygame.time.set_timer(difficulty_timer, 10000)

# ���� ��������� ��������
run = True
win = False
alive = True

while run:
    interval = 100  # ����� ��� ����������� ����������� ��������
    clock.tick(30)
    bear_hitbox = move_down[0].get_rect(topleft=(bear_x, bear_y)) # �������� �������� ���������
    mouse = pygame.mouse.get_pos()    

    # ������������ ������ ���
    screen.blit(background,(0,background_y))
    screen.blit(background,(0,background_y + 1000))

    if alive:
        # ��������� ������ ������, ���� ����� ������������ ����
        pygame.mixer.music.unpause()
        
        # ���������� �����������
        if obstacles:
            for (i, el) in enumerate (obstacles):
                screen.blit(obstacle, el)
                el.y -= level_speed
                if el.y <= -140:
                    obstacles.pop(i)
                if bear_hitbox.colliderect(el):
                    alive = False
        
        # ���������� �����������
        if bees:
            for (i, el) in enumerate (bees):
                screen.blit(bee[bee_frame], el)
                el.y -= level_speed
                if el.y <= -140:
                    bees.pop(i)
                if bear_hitbox.colliderect(el):
                    alive = False
                    
        # ���������� ����������� ��������
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

        # ���������� ��������, ��������� ����������� ����������� � ������� � �������� 0 �� �������� 3, �������� ��� ����� �������������� ��������� ��� ������ �������� � ����� ����.
        if bear_frame == 3:
            bear_frame = 0
            bee_frame = 0 # ��� ��������� ����������� ����, ��������� � ����� ���������� ���������� ���������� ������ �������� ��� �������������� �� ������ � ���� �� ��������
        elif pygame.time.get_ticks() - last_update > interval: # ��������� ���������, ����� �������� ��������� ��� �� � ��� �� �������� ��� clock.tick 
            bear_frame += 1
            bee_frame += 1
            last_update = pygame.time.get_ticks()
            
        # ������������ ����, ��������� ������� �����������.
        background_y -= level_speed
        if background_y <= -1000:
            background_y = 0

        # ������� ���������� ���������. ��������� ������� ��� ������������ ���������
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

        # ��������� ������� ��� ������������ �� ������
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
            
        # ��������
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

        # ��������� ���������� ������ 
        ammo_text = label.render(f"Shots left: {projectiles_amount}", True, (255,255,255))
        screen.blit(ammo_text, (10,10))

        ammo_text = label.render(f"Bees killed: {bees_amount}/10", True, (255,255,255))
        screen.blit(ammo_text, (265,930))

    # ������������� ���� ��� ���������
    elif bees_amount < 10:
        screen.fill((69, 124, 155))
        screen.blit(gameover_text,(315, 280))
        screen.blit(again_text, again_text_rect)
        pygame.mixer.music.pause()
        pygame.mixer.music.rewind() # ����� ��� ���� ����� ������ �� ������������ � ���� ����� �� ������� ������������ � ������ ���������
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

    # ������������� ���� ��� ������
    elif bees_amount >= 10: 
        screen.fill((69, 124, 155))
        screen.blit(win_text,(338, 280))
        screen.blit(again_text, again_text_rect)
        pygame.mixer.music.pause()
        pygame.mixer.music.rewind # ����� ��� ���� ����� ������ �� ������������ � ���� ����� �� ������� ������������ � ������ ���������
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

    # ���������� ������� ������ � �������
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        # ��������� ������
        if i.type == obstacle_timer:
            obstacles.append(obstacle.get_rect(topleft=(random.randint(0,810), 1000)))
            pygame.time.set_timer(obstacle_timer, time_to_spawn) 
            time_to_spawn = random.randint(spawn_speed,spawn_speed*2)
        # ��������� ��������
        if i.type == ammo_timer:
            ammo_boxes.append(ammo.get_rect(topleft=(random.randint(0,810),1000)))
            pygame.time.set_timer(ammo_timer, ammo_spawn)
            ammo_spawn = random.randint(5000,15000)
        # ��������� �����������
        if i.type == bee_timer:
            bees.append(bee[0].get_rect(topleft=(random.randint(0,810),1000)))
            pygame.time.set_timer(bee_timer, bee_spawn)
            bee_spawn = random.randint(spawn_speed*2,spawn_speed*4)
        # ��������� ���� ���������� ��������� ����� ���� ����������    
        if i.type == difficulty_timer:
            if level_speed <= 10:
                level_speed += 1
                spawn_speed -= 200
        # �������� �������� ��� ��������
        if alive and i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE and projectiles_amount > 0:
            projectiles.append(projectile.get_rect(topleft = (bear_x+44, bear_y+65)))
            projectiles_amount -= 1
            shot.play()

pygame.quit()
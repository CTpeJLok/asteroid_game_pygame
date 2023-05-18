import pygame
from pygame import Color

from Player import Player
from Enemy import Enemy
from Boom import Boom
from Welcome import Welcome
from utils import get_random_position, load_sprite, print_text
from settings import *


def create_and_get_player():
    return Player((SCREEN.WIDTH / 2, SCREEN.HEIGHT / 2), bullets.append)


def create_and_get_enemy():
    while True:
        position = get_random_position(screen)
        if position.distance_to(player.position) > PLAYER.MIN_DISTANCE_TO_ENEMY:
            break

    return Enemy(position, enemies.append)


def print_up():
    print_text(screen, -SCREEN.WIDTH / 2, -SCREEN.HEIGHT / 2, 'l', f'Количество жизней: {hearts}', font32,
               color=Color(COLOR.RED))
    print_text(screen, SCREEN.WIDTH / 2, -SCREEN.HEIGHT / 2, '', f'Количество очков: {score}', font32,
               color=Color(COLOR.YELLOW))


pygame.init()
pygame.display.set_caption(SCREEN.NAME)
screen = pygame.display.set_mode((SCREEN.WIDTH, SCREEN.HEIGHT))
background = load_sprite("screen", "0", False)
clock = pygame.time.Clock()
font32 = pygame.font.Font(None, 32)
font16 = pygame.font.Font(None, 16)
hearts = GAME.HEARTS
score = int(GAME.SCORE)
last_score = int(GAME.SCORE)

enemies = []
bullets = []
booms = []
player = create_and_get_player()
welcome = Welcome((SCREEN.WIDTH / 2, SCREEN.HEIGHT / 2))

for i in range(GAME.MAX_ENEMIES):
    enemies.append(create_and_get_enemy())

isPause = True
while isPause:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            quit()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            print(pos)
            correct_pos_x = range(int(welcome.position.x) - int(welcome.radius),
                                  int(welcome.position.x) + int(welcome.radius))
            correct_pos_y = range(int(welcome.position.y) - int(welcome.radius) + 100,
                                  int(welcome.position.y) + int(welcome.radius) - 100)
            if pos[0] in correct_pos_x and pos[1] in correct_pos_y:
                isPause = False

    # draw
    screen.blit(background, (0, 0))
    print_up()
    welcome.draw(screen)

    pygame.display.flip()
    clock.tick(SCREEN.FPS)

welcome = None

while True:
    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            quit()
        elif player and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()

    is_key_pressed = pygame.key.get_pressed()

    if player:
        if is_key_pressed[pygame.K_RIGHT]:
            player.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            player.rotate(clockwise=False)

        player.isAcceleration = is_key_pressed[pygame.K_LSHIFT]

        if is_key_pressed[pygame.K_UP]:
            player.front()
        elif is_key_pressed[pygame.K_DOWN]:
            player.back()

    # main
    # move
    if hearts > 0:
        for game_object in enemies:
            game_object.move(screen)

        for game_object in bullets:
            game_object.move(screen)

        if player:
            player.move(screen)

    # destroy enemies
    for bullet in bullets:
        for enemy in enemies:
            if enemy.collides_with(bullet):
                booms.append(Boom(enemy.position))
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += GAME.SCORE_PLUS
                if int(score / GAME.SCORE_UP) > int(last_score / GAME.SCORE_UP):
                    GAME.MAX_ENEMIES += GAME.ENEMIES_UP
                    last_score = int(score)

                if player:
                    enemies.append(create_and_get_enemy())
                break

    # check is player destroy
    if player:
        for enemy in enemies:
            if enemy.collides_with(player):
                hearts -= GAME.HEARTS_MINUS
                score += GAME.SCORE_PLUS_DESTROY
                if int(score / GAME.SCORE_UP) > int(last_score / GAME.SCORE_UP):
                    GAME.MAX_ENEMIES += GAME.ENEMIES_UP
                    last_score = int(score)

                if hearts > 0:
                    player = create_and_get_player()
                else:
                    player = None

                booms.append(Boom(enemy.position))
                enemies.remove(enemy)

                if player:
                    enemies.append(create_and_get_enemy())
                break

    # destroy bullet if out screen
    for bullet in bullets:
        if not screen.get_rect().collidepoint(bullet.position):
            bullets.remove(bullet)

    while len(enemies) < GAME.MAX_ENEMIES and hearts > 0:
        enemies.append(create_and_get_enemy())

    # draw
    screen.blit(background, (0, 0))

    for game_object in enemies:
        game_object.draw(screen)

    for game_object in bullets:
        game_object.draw(screen)

    for game_object in booms:
        if game_object.is_end():
            booms.remove(game_object)
            break
        game_object.draw(screen)

    if player:
        player.draw(screen)

    print_up()

    control = [
        'ESCAPE - выход',
        'LSHIFT - ускорение',
        'Пробел - стрелять',
        'Вперед, назад - движение',
        'Влево, вправо - поворот',
    ]
    for i in range(len(control)):
        print_text(screen, -SCREEN.WIDTH / 2, SCREEN.HEIGHT / 2 - 20 * i, 'ld', control[i], font32,
                   color=Color(COLOR.GREEN))

    pygame.display.flip()
    clock.tick(SCREEN.FPS)

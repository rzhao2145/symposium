import pygame
import os
import random
import blood
import player
import zombie
import missile
import devil
from zombie import Zombie
from devil import Devil
from sprites import *
from pygame import gfxdraw

from message import blit_text


os.environ['SDL_VIDEO_CENTERED'] = '1'

screen_width = 500
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
RED = (250, 20 , 0)

clock = pygame.time.Clock()
shot_clock = pygame.time.Clock()


zombies = pygame.sprite.Group()
devils = pygame.sprite.Group()
missiles = pygame.sprite.Group()


pygame.init()
my_font = pygame.font.SysFont("kalinga", 16)

p = player.Player()


def start_screen():
    global blood
    global my_font
    fade = False
    start = True
    alph = 0
    alphaSurface = pygame.Surface((500, 500))  # The custom-surface of the size of the screen.
    alphaSurface.fill((255, 255, 255))  # Fill it with whole white before the main-loop.
    alphaSurface.set_alpha(0)
    blood_sprites = pygame.sprite.Group()

    for i in range(3):
        bld = blood.Blood()
        bld.rect.x = random.randrange(screen_width)
        random.randrange(screen_height)
        blood_sprites.add(bld)
        pygame.display.flip()

    #my intro

    while not fade:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if pygame.time.get_ticks() > 1000 and not fade:
            fade = True
            print('go')
        else:
            screen.fill((0, 0, 0))  # At each main-loop fill the whole screen with black.
            alph += 1  # Increment alpha by a really small value (To make it slower, try 0.01)
            alphaSurface.set_alpha(alph)  # Set the incremented alpha-value to the custom surface.
            screen.blit(alphaSurface, (0, 0))  # Blit it to the screen-surface (Make them separate)

        pygame.display.flip()


    #stuff to put on start screen

    name = my_font.render("Created by Raymond Zhao", True, (0, 0, 0))
    start_text = my_font.render("Start", True, RED)

    while start:
        screen.fill(WHITE)
        screen.blit(name, (0,480))
        screen.blit(start_text, (230,240))
        screen.blit(boxpic, (100,50))
        button = pygame.gfxdraw.aaellipse(screen, 250, 250, 50, 20, RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 200 and pos[0] <= 300:
                    if pos[1] >= 230 and pos[1] <= 270:
                        start = False

        for blood in blood_sprites:
            screen.blit(blood.image, (blood.rect.x, blood.rect.y))
            blood.update()
            pygame.display.flip()

        pygame.display.flip()


def game_loop():
    done = False
    blood_spots = []
    can_shoot = True
    last_shot = 1000
    while True:
        clock.tick(60)
        screen.fill(WHITE)

        if not done:
            create_zombies()
            create_devils()
            done = True

        for zombs in zombies:
            zombs.move_towards_player(p)
            screen.blit(zombs.image, (zombs.rect.x, zombs.rect.y))
            if zombs.rect.colliderect(p.rect):
                blood_spots.append((zombs.rect.x,zombs.rect.y))
                p.get_hit()
                zombs.kill()



                print('you got hit')


        for devs in devils:
            devs.move_towards_player(p)
            screen.blit(devs.image, (devs.rect.x, devs.rect.y))
            if devs.rect.colliderect(p.rect):
                blood_spots.append((devs.rect.x,devs.rect.y))
                p.get_hit()
                devs.kill()
                print('you got hit')

            if pygame.time.get_ticks() - devs.last_shot >= 2000:
                chance = random.random()
                if chance < .05:
                    devs.last_shot = pygame.time.get_ticks()
                    m = missile.Missile(p, devs)
                    missiles.add(m)


        for spots in blood_spots:
            screen.blit(bloodpic, (spots[0],spots[1]))

        for m in missiles:
            m.update()
            screen.blit(m.image, (m.rect.x, m.rect.y))
            for zombs in zombies:
                if m.target == "enemy":
                    if zombs.rect.colliderect(m.rect):
                        blood_spots.append((zombs.rect.x, zombs.rect.y))
                        zombs.kill()
                        m.kill()
            for devs in devils:
                if m.target == "enemy":
                    if devs.rect.colliderect(m.rect):
                        blood_spots.append((devs.rect.x, devs.rect.y))
                        devs.kill()
                        m.kill()
            if p.rect.colliderect(m.rect):
                if m.target == "player":
                    p.get_hit()
                    m.kill()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(p.image, (p.rect.x,p.rect.y))
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_a] and not pressed[pygame.K_w] and not pressed[pygame.K_s]:
            p.move('a')
            p.image = player_left_pic
            p.dir = 'a'

        if pressed[pygame.K_w]:
            if pressed[pygame.K_a]:
                p.move('wa')
                p.image = player_upleft_pic
                p.dir = 'wa'
            elif pressed[pygame.K_d]:
                p.move('wd')
                p.image = player_upright_pic
                p.dir = 'wd'
            else:
                p.move('w')
                p.image = player_up_pic
                p.dir = 'w'

        if pressed[pygame.K_s]:
            if pressed[pygame.K_a]:
                p.move('sa')
                p.image = player_downleft_pic
                p.dir = 'sa'
            elif pressed[pygame.K_d]:
                p.move('sd')
                p.image = player_downright_pic
                p.dir = 'sd'
            else:
                p.move('s')
                p.image = player_down_pic
                p.dir = 's'

        if pressed[pygame.K_d] and not pressed[pygame.K_w] and not pressed[pygame.K_s]:
            p.move('d')
            p.image = player_right_pic
            p.dir = 'd'


        if pressed[pygame.K_SPACE]:
            if pygame.time.get_ticks() - last_shot >= 200:
                last_shot = pygame.time.get_ticks()
                shot_clock.tick()
                m = missile.Missile(p,'player')
                missiles.add(m)

        p.draw_health(screen)
        pygame.display.flip()

def create_zombies():
    for i in range(11):
        z = zombie.Zombie()
        z.rect.x = random.randint(0,500)
        z.rect.y = random.randint(0,500)
        zombies.add(z)

def create_devils():
    for i in range(6):
        d = devil.Devil()
        d.rect.x = random.randint(0,500)
        d.rect.y = random.randint(0,500)
        devils.add(d)




start_screen()
game_loop()
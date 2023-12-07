"""
the main loop should be here
"""

from object import Object
from object import Main_character
from object import NPC
import pygame as pg

WIDTH = 1280
HEIGHT = 720
FPS = 30

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.transform.scale(pg.image.load("pictures/map.png"), (WIDTH, HEIGHT))
desk_image = pg.transform.scale(pg.image.load("pictures/Desk.png"), (170, 110))
hero_image = pg.transform.scale(pg.image.load("pictures/prep1.png"), (75, 145))
clock = pg.time.Clock()
finished = False
objects =[]
Table = Object(screen, desk_image)
objects.append(Table)

npc = NPC(Object(screen, hero_image))
objects.append(npc.obj)


hero = Main_character(screen, hero_image)
hero.speed.y=30
hero.speed.x=30
Akey = 0
Skey = 0
Dkey = 0
Wkey = 0
Kspace = 0


while not finished:
    # TODO
    #drawing of objects should be here
    screen.blit(background, (0, 0))
    for obj in objects:
        obj.draw()
    hero.draw()
    pg.display.update()
    # Reaction to keys
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.KEYDOWN:
            if (event.key == pg.K_SPACE):
                if (Kspace):
                    Kspace = 0
                else:
                    Kspace = 1
            if event.key == pg.K_a:
                Akey = 1
            if event.key == pg.K_s:
                Skey = 1
            if event.key == pg.K_d:
                Dkey = 1
            if event.key == pg.K_w:
                Wkey = 1
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a:
                Akey = 0
            if event.key == pg.K_s:
                Skey = 0
            if event.key == pg.K_d:
                Dkey = 0
            if event.key == pg.K_w:
                Wkey = 0

    hero.move(objects, Akey, Wkey, Skey, Dkey)
    npc.move()
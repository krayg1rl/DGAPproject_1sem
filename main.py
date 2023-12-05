"""
the main loop should be here
"""
import pygame as pg
WIDTH = 1280
HEIGHT = 720
FPS = 30

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.transform.scale(pg.image.load("images/background.jpg"), (WIDTH, HEIGHT))
clock = pg.time.Clock()
finished = False

Akey = 0
Skey = 0
Dkey = 0
Wkey = 0
Kspace = 0

while not finished:
    # TODO
    #drawing of objects should be here

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
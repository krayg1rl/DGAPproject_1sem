"""
the main loop should be here
"""

from object import Object
from object import Main_character
import pygame as pg
import time

WIDTH = 1280
HEIGHT = 720
FPS = 30

TIME_LIMIT = 600  # In seconds

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.transform.scale(pg.image.load("pictures/map.png"), (WIDTH, HEIGHT))
desk_image = pg.transform.scale(pg.image.load("pictures/Desk.png"), (100, 100))

clock = pg.time.Clock()

objects = []

Table = Object(screen, desk_image)
objects.append(Table)

# Font for displaying timer on board
timer_font = pg.font.SysFont('calibri', 50)

start_time = pg.time.get_ticks()
time_left = TIME_LIMIT

finished = False

hero = Main_character(screen)
hero.speed.y = 30
hero.speed.x = 30

# keys_pressed is dictionary with following structure:
# keys_pressed = {'KeyName': <Pressed or not(boolean)>}
keys_pressed = {'SPACE': False, 'Akey': False, 'Skey': False, 'Dkey': False, 'Wkey': False}


def handle_events(events):
    '''
    function, which is aimed at managing keyboard(or mouse) events and proper responses for them
    '''

    global finished, keys_pressed

    for event in events:
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if keys_pressed['SPACE']:
                    keys_pressed['SPACE'] = True
                else:
                    keys_pressed['SPACE'] = False
            if event.key == pg.K_a:
                keys_pressed['Akey'] = True
            if event.key == pg.K_s:
                keys_pressed['Skey'] = True
            if event.key == pg.K_d:
                keys_pressed['Dkey'] = True
            if event.key == pg.K_w:
                keys_pressed['Wkey'] = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a:
                keys_pressed['Akey'] = False
            if event.key == pg.K_s:
                keys_pressed['Skey'] = False
            if event.key == pg.K_d:
                keys_pressed['Dkey'] = False
            if event.key == pg.K_w:
                keys_pressed['Wkey'] = False

    hero.move(objects, keys_pressed['Akey'], keys_pressed['Wkey'], keys_pressed['Skey'], keys_pressed['Dkey'])


def timer():
    global start_time, time_left

    if time_left <= 0:
        start_time = pg.time.get_ticks()
        time_left = TIME_LIMIT

    time_left = TIME_LIMIT - ((pg.time.get_ticks()-start_time)/1000)

    time_passed = timer_font.render('Timer: ' + str(round(time_left, 2)), True, (255, 255, 255, 255))

    screen.blit(time_passed, (180, 53))


while not finished:
    # TODO
    #drawing of objects should be here
    screen.blit(background, (0, 0))

    timer()

    for obj in objects:
        obj.draw()
    hero.draw()
    pg.display.update()
    # Reaction to keys
    clock.tick(FPS)

    handle_events(pg.event.get())

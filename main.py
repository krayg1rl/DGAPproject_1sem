"""
the main loop should be here
"""

from object import *
import menu
import pygame as pg
import time

WIDTH = 1280
HEIGHT = 720
FPS = 30

TIME_LIMIT = 120  # In seconds

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.transform.scale(pg.image.load("pictures/map.png"), (WIDTH, HEIGHT))
# TODO
# add image for main menu
menu_background = pg.transform.scale(pg.image.load("pictures/map.png"), (WIDTH, HEIGHT))
desk_image = pg.transform.scale(pg.image.load("pictures/Desk.png"), (170, 110))
prep_image = pg.transform.scale(pg.image.load("pictures/prep2.png"), (100, 125))
scanner_image = pg.transform.scale(pg.image.load("pictures/radar.png"), size=(340, 250))

# load button images
options_img = pg.image.load("pictures/button_options.png").convert_alpha()

# initialiasating buttons
options_button = menu.Button(297, 250, options_img, 1)

clock = pg.time.Clock()

objects = []

physical_objects = []
visible_objects = []

tables = []

for i in desks:
    table = Object(screen, desk_image)
    table.setPos(i.x, i.y)
    visible_objects.append(table)
    physical_objects.append(table)

npc = NPC(Object(screen, prep_image), Object(screen, scanner_image))
visible_objects.append(npc.obj)
visible_objects.append(npc.sc_visible)

# Font for displaying timer on board
timer_font = pg.font.SysFont('calibri', 50)
points_font =pg.font.SysFont('calibri', 50)

start_time = pg.time.get_ticks()
time_left = TIME_LIMIT

finished = False
menu_state = 'main'

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
                keys_pressed['SPACE'] = True
            if event.key == pg.K_a:
                keys_pressed['Akey'] = True
            if event.key == pg.K_s:
                keys_pressed['Skey'] = True
            if event.key == pg.K_d:
                keys_pressed['Dkey'] = True
            if event.key == pg.K_w:
                keys_pressed['Wkey'] = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                keys_pressed['SPACE'] = False
            if event.key == pg.K_a:
                keys_pressed['Akey'] = False
            if event.key == pg.K_s:
                keys_pressed['Skey'] = False
            if event.key == pg.K_d:
                keys_pressed['Dkey'] = False
            if event.key == pg.K_w:
                keys_pressed['Wkey'] = False

    hero.cheat(keys_pressed['SPACE'])

    print(hero.points)
    hero.move(physical_objects, keys_pressed['Akey'], keys_pressed['Wkey'], keys_pressed['Skey'], keys_pressed['Dkey'])
    npc.move()


def timer():
    global start_time, time_left

    if time_left <= 0:
        start_time = pg.time.get_ticks()
        time_left = TIME_LIMIT

    time_left = TIME_LIMIT - ((pg.time.get_ticks()-start_time)/1000)

    time_left_minutes = str(int(int(time_left) // 60))
    time_left_seconds = str(int(int(time_left) % 60))
    time_left_milliseconds = str(int((time_left - 60 * int(time_left_minutes) - int(time_left_seconds)) * 100) % 100)

    if len(time_left_seconds) == 1:
        time_left_seconds = '0' + time_left_seconds
    if len(time_left_minutes) == 1:
        time_left_minutes = '0' + time_left_minutes
    if len(time_left_milliseconds) == 1:
        time_left_milliseconds = '0' + time_left_milliseconds

    time_passed = timer_font.render('Timer: ' + time_left_minutes + ':' + time_left_seconds + ':' + time_left_milliseconds, True, (255, 255, 255, 255))

    screen.blit(time_passed, (WIDTH / 7.11, HEIGHT / 13.585))


while not finished:
    # TODO
    # drawing of objects should be here

    clock.tick(FPS)

    if menu_state == 'game':
        screen.blit(background, (0, 0))

        timer()

        hero_point = str(hero.points)
        points = points_font.render(hero_point, True, (255, 255, 255, 255))
        screen.blit(points, (1000, 53))

        for obj in visible_objects:
            obj.draw()
        hero.draw()

    if menu_state == 'main':
        screen.blit(menu_background, (0, 0))

        if options_button.draw(screen):
            menu_state = "game"

    handle_events(pg.event.get())

    pg.display.update()

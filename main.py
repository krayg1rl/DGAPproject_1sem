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

TIME_LIMIT = 300  # In seconds

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.transform.scale(pg.image.load("pictures/map.png"), (WIDTH, HEIGHT))
menu_background = pg.transform.scale(pg.image.load("pictures/Main_menu.png"), (WIDTH, HEIGHT))
pause_menu_background = pg.transform.scale(pg.image.load("pictures/pause_sreen.jpg"), (WIDTH, HEIGHT))
desk_image = pg.transform.scale(pg.image.load("pictures/Desk.png"), (170, 110))
prep_image = pg.transform.scale(pg.image.load("pictures/prep2.png"), (100, 125))

npc_image = []
npc_size = (70, 65)
npc_image.append(pg.transform.scale(pg.image.load("pictures/NPC_1_fixed.png"), (80, 60)))
npc_image.append(pg.transform.scale(pg.image.load("pictures/NPC_2_fixed.png"), (80, 60)))
npc_image.append(pg.transform.scale(pg.image.load("pictures/NPC_3_fixed.png"), (80, 60)))
npc_image.append(pg.transform.scale(pg.image.load("pictures/NPC_4_fixed.png"), (80, 60)))
npc_image.append(pg.transform.scale(pg.image.load("pictures/NPC_5_fixed.png"), (80, 60)))

npc_highlited = []
npc_highlited.append(pg.transform.scale(pg.image.load("pictures/NPC_1_triggered.png"), (80, 60)))
npc_highlited.append(pg.transform.scale(pg.image.load("pictures/NPC_2_triggered.png"), (80, 60)))
npc_highlited.append(pg.transform.scale(pg.image.load("pictures/NPC_3_triggered.png"), (80, 60)))
npc_highlited.append(pg.transform.scale(pg.image.load("pictures/NPC_4_triggered.png"), (80, 60)))
npc_highlited.append(pg.transform.scale(pg.image.load("pictures/NPC_5_triggered.png"), (80, 60)))


scanner_image = pg.transform.scale(pg.image.load("pictures/radar.png"), size=(340, 250))
chair_img = pg.transform.scale(pg.image.load("pictures/Chair.png"), size=(50,100))
chair_highlight = pg.transform.scale(pg.image.load("pictures/Chair_highlight.png"), size=(50,100))
karasev_img = pg.transform.scale(pg.image.load("pictures/Karasev_dialogue.PNG"), (WIDTH/2, HEIGHT/2))
ershov_img=pg.transform.scale(pg.image.load("pictures/Ershov_dialogue.PNG"), (WIDTH/2, HEIGHT/2))
kiselev_img=pg.transform.scale(pg.image.load("pictures/Kiselev.png"), size=(250, 250))
kiselev_rect=kiselev_img.get_rect(center = (200, 200))
# load button images
settings_button_img = pg.image.load("pictures/settings_button.png").convert_alpha()
settings_button_text_img = pg.image.load("pictures/settings_button_text.png").convert_alpha()
quit_button_img = pg.image.load("pictures/quit_button.png").convert_alpha()
start_game_button_img = pg.image.load("pictures/start_button.png").convert_alpha()
pause_game_button_img = pg.image.load("pictures/pause_button.png").convert_alpha()
continue_game_button_img = pg.image.load("pictures/continue_game_button.png").convert_alpha()
restart_button_img = pg.image.load("pictures/restart_button.png").convert_alpha()
return_button_img = pg.image.load("pictures/return_button.png").convert_alpha()
info_button_img = pg.image.load("pictures/info_button.png").convert_alpha()
a_button_img = pg.image.load("pictures/A_img.png").convert_alpha()
b_button_img = pg.image.load("pictures/B_img.png").convert_alpha()
c_button_img = pg.image.load("pictures/C_img.png").convert_alpha()
d_button_img = pg.image.load("pictures/D_img.png").convert_alpha()
questions=[]
questions_rect = []
right_answers=[]
after_true_answ=[]
after_false_answ=[]
question1 = pg.transform.scale(pg.image.load("pictures/question1.png"), (WIDTH*0.75, HEIGHT*0.75))
questions_rect.append(question1.get_rect(center =(WIDTH/2, HEIGHT/2)))
questions.append(question1)
right_answers.append('B')
after_true_answ.append(question1)

# initialiasating buttons
settings_button = menu.Button(WIDTH / 3, HEIGHT / 3, settings_button_img, 1)
settings_button_text = menu.Button(WIDTH / 2, HEIGHT / 2 + 30, settings_button_text_img, 6.5)
quit_button = menu.Button(WIDTH / 2, HEIGHT / 2 + 130, quit_button_img, 6.2)
start_game_button = menu.Button(WIDTH / 2, HEIGHT / 2 - 80, start_game_button_img, 7.4)
pause_game_button = menu.Button(WIDTH - pause_game_button_img.get_width() * 3 / 2 - 13, pause_game_button_img.get_height() * 3 / 2 + 13,
                                pause_game_button_img, 3)
continue_game_button = menu.Button(WIDTH - pause_game_button_img.get_width() * 3 / 2 - 13, pause_game_button_img.get_height() * 3 / 2 + 14,
                                   continue_game_button_img, 3)
return_button = menu.Button(WIDTH / 2 - 95, HEIGHT / 3 + 28, return_button_img, 6)
restart_button = menu.Button(WIDTH / 2 - 95, HEIGHT / 2 + 3, restart_button_img, 6)
quit_button_pause = menu.Button(WIDTH / 2 - 95, HEIGHT / 2 + 93, quit_button_img, 5.5)
info_button = menu.Button(120, 80, info_button_img, 5)
buttons_height = HEIGHT*0.75
a_button = menu.Button(WIDTH/2-100, buttons_height, a_button_img, 1)
b_button = menu.Button(WIDTH/2, buttons_height, b_button_img, 1)
c_button = menu.Button(WIDTH/2+100, buttons_height, c_button_img, 1)
d_button = menu.Button(WIDTH/2+200, buttons_height, d_button_img, 1)
clock = pg.time.Clock()

objects = []

physical_objects = []
visible_objects = []

interactives = []

for i in desks:
    table = Object(screen, desk_image)
    table.setPos(i.x, i.y)
    visible_objects.append(table)
    physical_objects.append(table)

for i in chairs:
    chair = Object(screen, chair_img)
    chair.draw_order = 1
    chair.setPos(i.x, i.y)
    chair.add_image(chair_highlight)
    visible_objects.append(chair)
    interactives.append(Interactive(chair))

num_of_students = 3
students = []
for i in range(num_of_students):
    sprite_num = rd.randint(0, 4)
    students.append(Student(Object(screen, npc_image[sprite_num])))
    students[i].obj.add_image(npc_highlited[sprite_num])
    students[i].occupy_place(interactives)
    visible_objects.append(students[i].obj)

npc = NPC(Object(screen, prep_image))
karasev = Teacher(npc, Object(screen, scanner_image), karasev_img)
visible_objects.append(npc.obj)
visible_objects.append(karasev.sc_visible)

visible_objects.sort(key= lambda x: x.draw_order)


# Font for displaying timer on board
timer_font = pg.font.SysFont('calibri', 50)
points_font =pg.font.SysFont('calibri', 50)

start_time = pg.time.get_ticks()
time_left = TIME_LIMIT

finished = False
menu_state = 'main'

hero = Main_character(screen)
hero.speed.y = 7
hero.speed.x = 7
hero.chance = 3

num_of_q=0
# keys_pressed is dictionary with following structure:
# keys_pressed = {'KeyName': <Pressed or not(boolean)>}
keys_pressed = {'SPACE': False, 'Akey': False, 'Skey': False, 'Dkey': False, 'Wkey': False, 'Qkey': False}


def handle_events(events):
    '''
    function, which is aimed at managing keyboard(or mouse) events and proper responses for them
    '''

    global finished, keys_pressed, menu_state

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
            if event.key == pg.K_q:
                keys_pressed['Qkey'] = True
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
            if event.key == pg.K_q:
                keys_pressed['Qkey'] = False

    for i in interactives:
        i.interact(hero, keys_pressed['Qkey'])

    for student in students:
        student.check_for_character(hero)

    hero.cheat(keys_pressed['SPACE'] and hero.near_student and hero.sitting)

    # print(hero.points)
    hero.move(physical_objects, keys_pressed['Akey'], keys_pressed['Wkey'], keys_pressed['Skey'], keys_pressed['Dkey'], keys_pressed['SPACE'])

    karasev.move()
    if(karasev.check(hero) and keys_pressed['SPACE']):
        hero.chance = hero.chance-1
        keys_pressed['SPACE']=0
        keys_pressed['Akey']=0
        keys_pressed['Wkey'] = 0
        keys_pressed['Skey'] = 0
        keys_pressed['Dkey'] = 0
        menu_state = 'quiz'


def restart_game():
    '''
    function which set all parameters to initial values
    '''
    global start_time

    start_time = pg.time.get_ticks()
    hero.points = 0


def timer():
    global start_time, time_left

    if time_left <= 0:
        # place to call function which reacts on the end of time
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

    clock.tick(FPS)

    if menu_state == 'game':
        screen.blit(background, (0, 0))

        timer()

        hero_point = str(float(int(hero.points))/1000.0)
        points = points_font.render(hero_point, True, (255, 255, 255, 255))
        screen.blit(points, (1000, 53))

        for obj in visible_objects:
            obj.draw()
        hero.draw()
        if(hero.sitting):
            screen.blit(hero.chair.images[0], hero.chair.position)

        handle_events(pg.event.get())
        if(hero.chance<=2):
            screen.blit(karasev_img, (WIDTH/2,HEIGHT/2))
        if(hero.chance<=1):
            screen.blit(ershov_img, (WIDTH/12,HEIGHT/2))

        if((time_left)<280) and ((time_left)>260):


            screen.blit(kiselev_img, kiselev_rect)
            pg.draw.line(screen, (255,0,0), (kiselev_rect.centerx,kiselev_rect.centery-30), ((50*(time_left-260)), HEIGHT), 4)
            pg.draw.line(screen, (255, 0, 0), (kiselev_rect.centerx + 40, kiselev_rect.centery-30), ((50 * (time_left - 260)+40), HEIGHT), 4)

        if pause_game_button.draw(screen):
            menu_state = 'pause'
            pause_time = pg.time.get_ticks()
            continue_game_button.clicked = True

    elif menu_state == 'pause':

        screen.blit(pause_menu_background, (0, 0))

        new_start_time = (pg.time.get_ticks() - pause_time)

        if continue_game_button.draw(screen):
            menu_state = 'game'
            start_time += new_start_time
        if return_button.draw(screen):
            menu_state = 'game'
            settings_button_text.clicked = True
        if restart_button.draw(screen):
            restart_game()
            menu_state = 'game'
        if quit_button_pause.draw(screen):
            menu_state = 'main'

        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True

    elif menu_state == 'main':
        screen.blit(menu_background, (0, 0))

        if settings_button_text.draw(screen):
            menu_state = 'options'
        if quit_button.draw(screen):
            finished = True
        if start_game_button.draw(screen):
            menu_state = 'game'
        if info_button.draw(screen):
            menu_state = 'info'

        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True

    elif menu_state == 'options':
        screen.blit(menu_background, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True

    elif menu_state == 'quiz':
        screen.blit(questions[num_of_q], questions_rect[num_of_q])
        if a_button.draw(screen):
            if(right_answers[num_of_q]=='A'):
                menu_state = 'game'
            else:
                pass
        if b_button.draw(screen):
            if (right_answers[num_of_q] == 'B'):
                menu_state = 'game'
            else:
                pass

        if c_button.draw(screen):
            if (right_answers[num_of_q] == 'C'):
                menu_state = 'game'
            else:
                pass
        if d_button.draw(screen):
            if (right_answers[num_of_q] == 'D'):
                menu_state = 'game'
            else:
                pass
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
        # screen.blit(questions[num_of_q], (1000, 1000))
        # if a_button.draw(screen):
        #     if(right_answers[num_of_q]=='A'):
        #         # after_true_answ.blit(screen,(0,0))








    pg.display.update()

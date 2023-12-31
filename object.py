import pygame as pg
import math
import random as rd
import menu

WIDTH = 1280
HEIGHT = 720

draw_order_changed = True

teacher_waypoints = [pg.Vector2(400, 75), pg.Vector2(1000, 75),
                     pg.Vector2(400, 260), pg.Vector2(1000, 260),
                     pg.Vector2(400, 445), pg.Vector2(1000, 445),
                     pg.Vector2(400, 630), pg.Vector2(1000, 630),
                     pg.Vector2(80, 75), pg.Vector2(700, 75),
                     pg.Vector2(80, 260), pg.Vector2(700, 260),
                     pg.Vector2(80, 445), pg.Vector2(700, 445),
                     pg.Vector2(80, 630), pg.Vector2(700, 630)]

desks = [pg.Vector2(200 + i%3*300, 210 + int(i/3)*185) for i in range(9)]

chairs = [pg.Vector2(215 + i%2*80 + int(i/2)%3*300 + rd.random()*10, 230 + int(i/6)*185 + rd.random()*15) for i in range(18)]

buttons_height = HEIGHT*0.75+110
buttons_size = 0.5
buttons_width = WIDTH/2+400
a_button_img = pg.image.load("pictures/A_img.png")
b_button_img = pg.image.load("pictures/B_img.png")
c_button_img = pg.image.load("pictures/C_img.png")
d_button_img = pg.image.load("pictures/D_img.png")
ovch_button_img=pg.image.load("pictures/ovch_ok.png")
a_button = menu.Button(buttons_width, buttons_height, a_button_img, buttons_size)
b_button = menu.Button(buttons_width+50, buttons_height, b_button_img, buttons_size)
c_button = menu.Button(buttons_width+100, buttons_height, c_button_img, buttons_size)
d_button = menu.Button(buttons_width+150, buttons_height, d_button_img, buttons_size)
ovch_button = menu.Button(WIDTH/2+500, buttons_height-50, ovch_button_img, 0.2)


# Game sounds
DEFAULT_SOUND_VOLUME = 0.5
pg.mixer.init()
cheating_sound = pg.mixer.Sound("sound/delta_alpha.ogg")
# Set a volume for all sounds
pg.mixer.Sound.set_volume(cheating_sound, 1 * DEFAULT_SOUND_VOLUME)
sounds_playing = {'cheating_sound': False}


def is_close(a, b, margin):
    return math.fabs(a-b) < margin

def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

        Args:
            surface (pygame.Surface): The surface that is to be rotated.
            angle (float): Rotate by this angle.
            pivot (tuple, list, pygame.math.Vector2): The pivot point.
            offset (pygame.math.Vector2): This vector is added to the pivot.
        """
    rot_img = pg.transform.rotate(surface, -angle)
    rot_offset = offset.rotate(angle)
    rect = rot_img.get_rect(center=pivot + rot_offset)
    return rot_img, rect

def contains(rect, point):
    """
    Checks if rect contains a point

        Args:
            rect(pg.Rect)
            point(pg.Vector2)
    """
    return  (rect.x < point.x < rect.x + rect.width) and (rect.y < point.y < rect.y + rect.height)

class Object:
    '''
    Object: anything that should be drawn or can interact with the hero
    '''
    def __init__(self, screen: pg.Surface, image):
        self.speed = pg.Vector2(0, 0)
        self.images = []
        self.images.append(image)
        self.position = self.images[0].get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen = screen
        self.anim_state = 0
        self.visible = True

        self.draw_order = 0 # objects with higher draw order are drawn later

    def draw(self):
        self.screen.blit(self.images[self.anim_state], self.position)

    def add_image(self, image):
        self.images.append(image)

    def get_anim_state(self):
        return self.anim_state

    def setPos(self, x, y):
        self.position.x = x
        self.position.y = y


class NPC:
    def __init__(self, object):
        self.obj = object

        self.pos = pg.Vector2(self.obj.position.x, self.obj.position.y)

        self.turn_speed = 15
        self.an = 0
        self.delta_an = 0
        self.target_an = 0
        self.waypoints = teacher_waypoints
        self.curr_target = pg.Vector2(self.obj.position.x, self.obj.position.y)
        self.vel_max = pg.Vector2(8, 8)
        self.max_sleepframes = 23
        self.sleepframes = 0

        self.state = 0  # 0=sleeping, 1=moving, 2=turning, 3=looking around

    def new_target(self, target):
        self.curr_target = target
        self.sleepframes = self.max_sleepframes

    def look_around(self):
        pass

    def move(self):
        self.obj.position.x = self.pos.x
        self.obj.position.y = self.pos.y
        if self.state == 0:
            if self.sleepframes > 0:
                self.sleepframes -= 1
            else:
                self.state = 1
        elif self.state == 1:
            if not is_close(self.an, self.target_an, self.turn_speed * 0.6):
                self.state = 2
            elif not is_close(self.curr_target.x, self.pos.x, self.vel_max.x * 0.6):
                self.target_an = 180 + 90 * math.copysign(1, self.curr_target.x - self.pos.x)
                self.pos.x += math.copysign(self.vel_max.x, self.curr_target.x - self.pos.x)
            elif not is_close(self.curr_target.y, self.pos.y, self.vel_max.y * 0.6):
                self.target_an = 90 - 90 * math.copysign(1, self.curr_target.y - self.pos.y)
                self.pos.y += math.copysign(self.vel_max.y, self.curr_target.y - self.pos.y)
            else:
                self.state = 0
                self.new_target(self.waypoints[rd.randint(0, len(teacher_waypoints) - 1)])
        if self.state == 2:
            if is_close(self.an, self.target_an, self.turn_speed * 0.6):
                self.state = 1
            else:
                if 0 > self.target_an - self.an > -180:
                    self.delta_an = -1
                else:
                    self.delta_an = 1
                self.delta_an *= self.turn_speed
                self.an += self.delta_an

                if self.an > 359:
                    self.an -= 360




class Teacher:
    def __init__(self, npc, scanner, dialog):
        self.npc = npc
        self.scanner = scanner
        self.scanpos = pg.Vector2(50, 15)
        self.sc_visible = Object(scanner.screen, scanner.images[0])
        self.dialogue = dialog
        self.look_angle = 90
        self.vision_range = 330

    def move(self):
        self.npc.move()
        self.sc_visible.images[0], new_rect = rotate(self.scanner.images[0], self.npc.an, self.npc.pos + self.scanpos, pg.Vector2(5, 120))
        self.sc_visible.position = new_rect

    def check(self, student):
        rel_pos = self.npc.pos + self.scanpos - pg.Vector2(student.position.x + student.position.width/2, student.position.y + student.position.height/2)
        rel_angle = math.atan2(rel_pos.y, rel_pos.x) * 180 / math.pi + 90
        if rel_angle < 0:
            rel_angle += 360
        ans = rel_pos.magnitude() < self.vision_range and is_close(rel_angle, self.npc.an, self.look_angle/2)
        return ans and (student.near_student or not student.sitting)

class Student:
    def __init__(self, object):

        self.obj = object
        self.interactive = Interactive(self.obj)
        self.interactive.int_box = pg.Rect(self.obj.position.x - 100, self.obj.position.y - 20, self.obj.position.width + 200, self.obj.position.height + 50)

        self.intellect = 0.5 + rd.random()*0.8
        self.cooperation = 0.4 + rd.random()*0.6

    def occupy_place(self, places):
        '''
        Args:
            places: array of possible "places" where student can sit
        '''
        ptr = rd.randint(0, len(places) - 1)
        if ptr%2 == 0:
            while (not places[ptr].can_interact) or (not places[ptr + 1].can_interact): # either of 2 chairs is occupied
                ptr = (ptr + 2)%len(places)
        else:
            while (not places[ptr].can_interact) or (not places[ptr - 1].can_interact):
                ptr = (ptr + 2)%len(places)

        places[ptr].can_interact = False
        self.interactive.set_pos(pg.Vector2(places[ptr].obj.position.x - 15, places[ptr].obj.position.y - 25))


    def check_for_character(self, character):
        if self.interactive.near_character(character):
            character.near_student = True
            character.point_speed = character.base_point_speed * self.intellect * self.cooperation
            if not character.sitting:
                self.obj.anim_state = 1
            else:
                self.obj.anim_state = 0
        else:
            self.obj.anim_state = 0

def occupy_place(character, places, not_availible):
    '''
    Args:
        places: array of possible "places" where student can sit
    '''
    ptr = rd.randint(0, len(places) - 1)
    if ptr%2 == 0:
        while (not places[ptr].can_interact) or (not places[ptr + 1].can_interact): # either of 2 chairs is occupied
            ptr = (ptr + 2)%len(places)
    else:
        while (not places[ptr].can_interact) or (not places[ptr - 1].can_interact):
            ptr = (ptr + 2)%len(places)
    if not_availible:
        places[ptr].can_interact = False
    character.interactive.set_pos(pg.Vector2(places[ptr].obj.position.x - 15, places[ptr].obj.position.y - 25))
    return ptr


class Interactive:
    '''
    class of objects that the player is able to interact with
    i.e. chairs or other students
    '''
    def __init__(self, object):
        '''

        Args:
            object(Object): object that has the interactive property
        '''
        self.can_interact = True
        self.obj = object
        self.int_box = pg.Rect(object.position)

    def set_pos(self, pos):
        '''
        Args:
            pos: pg.Vector2 - new position
        '''
        self.int_box.x += (pos.x - self.obj.position.x)
        self.int_box.y += (pos.y - self.obj.position.y)
        self.obj.setPos(pos.x, pos.y)

    def near_character(self, character):
        return self.int_box.colliderect(character.position)

    def interact(self, character, condition):
        '''
        interaction with the main character
        Args:
            character(Main_character):
            condition(bool):

        '''
        if self.near_character(character) and self.can_interact:
            if not character.sitting:
                self.obj.anim_state = 1
            else:
                self.obj.anim_state = 0
            if condition and character.state_change_cooldown == 0:
                character.state_change_cooldown = 15
                if not character.sitting:
                    character.oldpos.x = character.obj.position.x
                    character.oldpos.y = character.obj.position.y
                    character.obj.position.x = self.obj.position.x - 15
                    character.obj.position.y = self.obj.position.y - 25
                    character.sitting = True
                    character.obj.draw_order = 0
                    character.draw_order_changed = True

                    character.near_student = False
                    character.chair = self.obj
                else:
                    character.obj.position.x = character.oldpos.x
                    character.obj.position.y = character.oldpos.y
                    character.sitting = False
                    character.obj.draw_order = 3
                    character.draw_order_changed = True
            elif character.state_change_cooldown > 0:
                character.state_change_cooldown -= 1
        else:
            self.obj.anim_state = 0




class Main_character:

    def __init__(self, screen: pg.Surface):
        self.speed = pg.Vector2(0, 0)

        self.image = pg.transform.scale(pg.image.load("pictures/hero.png"), (80, 100))
        self.obj = Object(screen, self.image)
        self.obj.draw_order = 2
        self.interactive = Interactive(self.obj)
        self.draw_order_changed = False

        self.position = self.image.get_rect(center=(100, HEIGHT/2))
        self.position.height = self.position.height/2
        self.obj.position = self.position
        self.screen = screen
        self.points = 0
        self.base_point_speed = 2
        self.point_speed = self.base_point_speed
        self.chance = 0

        self.sitting = False
        self.near_student = False
        self.chair=None
        self.oldpos = pg.Vector2(0, 0)  # hero's coordinates before he sat down
        self.state_change_cooldown = 0  # for how many frames the hero can't change states (sit down or stand up)

    def meet_Obj(self,objects, Akey,Wkey, Skey, Dkey, leftcrash, rightcrash, topcrash, bottomcrash):
        for obj in objects:
            if ((self.obj.position.top < obj.position.bottom) and (self.obj.position.bottom > obj.position.top) and (
                    self.obj.position.left <= obj.position.right) and (self.obj.position.left >= obj.position.centerx)):
                leftcrash = True
            if ((self.obj.position.top < obj.position.bottom) and (self.obj.position.bottom > obj.position.top) and (
                    self.obj.position.right >= obj.position.left) and (self.obj.position.right <= obj.position.centerx)):
                rightcrash = True
            if ((self.obj.position.left < obj.position.right) and (self.obj.position.right > obj.position.left) and (
                    self.obj.position.top <= obj.position.bottom) and (self.obj.position.top >= obj.position.centery)):
                topcrash = True
            if ((self.obj.position.left < obj.position.right) and (self.obj.position.right > obj.position.left) and (
                    self.obj.position.bottom >= obj.position.top) and (self.obj.position.bottom <= obj.position.centery)):
                bottomcrash = True

        return leftcrash, rightcrash, bottomcrash, topcrash

    def move(self, objects, Akey, Wkey, Skey, Dkey, Space):
        leftcrash = 0
        rightcrash = 0
        bottomcrash = 0
        topcrash = 0

        self.obj.position = pg.Rect(self.obj.position.x, self.obj.position.y + self.obj.position.height,
                                    self.obj.position.width, self.obj.position.height)

        if not Space and not self.sitting:
            if (self.obj.position.left <= 0):
                leftcrash = True
            if (self.obj.position.right >= WIDTH):
                rightcrash = True
            if (self.obj.position.top <= 150):
                topcrash = True
            if (self.obj.position.bottom >= HEIGHT + 90):
                bottomcrash = True
            for obj in objects:
                if ((self.obj.position.top < obj.position.bottom) and (self.obj.position.bottom > obj.position.top) and (
                        self.obj.position.left <= obj.position.right) and (self.obj.position.left >= obj.position.centerx)):
                    leftcrash = True
                if ((self.obj.position.top < obj.position.bottom) and (self.obj.position.bottom > obj.position.top) and (
                        self.obj.position.right >= obj.position.left) and (self.obj.position.right <= obj.position.centerx)):
                    rightcrash = True
                if ((self.obj.position.left < obj.position.right) and (self.obj.position.right > obj.position.left) and (
                        self.obj.position.top <= obj.position.bottom) and (self.obj.position.top >= obj.position.centery)):
                    topcrash = True
                if ((self.obj.position.left < obj.position.right) and (self.obj.position.right > obj.position.left) and (
                        self.obj.position.bottom >= obj.position.top) and (self.obj.position.bottom <= obj.position.centery)):
                    bottomcrash = True

            if (Akey and not Dkey):
                if (leftcrash):
                    # self.position.x=self.position.x + self.speed.x
                    pass
                else:
                    self.obj.position.x -= self.speed.x
            elif (Dkey and not Akey):
                if (rightcrash):
                    # self.position.x = self.position.x -  self.speed.x
                    pass
                else:
                    self.obj.position.x += self.speed.x
            if (Wkey and not Skey):
                if (topcrash):
                    # self.position.y = self.position.y+self.speed.y
                    pass
                else:
                    self.obj.position.y -= self.speed.y
            elif (Skey and not Wkey):
                if (bottomcrash):
                    # self.position.y = self.position.y-self.speed.y
                    pass
                else:
                    self.obj.position.y += self.speed.y
        #self.obj.position = pg.Rect(self.position.x, self.position.y - self.position.height,
        #                        self.position.width, self.position.height)
        self.position = self.obj.position
        self.obj.position = pg.Rect(self.obj.position.x, self.obj.position.y - self.obj.position.height, self.obj.position.width, self.obj.position.height)





    def draw(self):
        self.screen.blit(self.image, (self.position.x, self.position.y - self.position.height))


    def cheat(self, condition):
        '''
        Args:
            condition(bool): if conditions for cheating are met
        '''
        global sounds_playing

        if(condition):
            if not sounds_playing['cheating_sound']:
                cheating_sound.play()
                sounds_playing['cheating_sound'] = True

            self.points += self.point_speed
        else:
            sounds_playing['cheating_sound'] = False
            cheating_sound.stop()


class Artifact:
    def __init__(self, objects, art_id):
        self.obj = objects[art_id]
        self.interactive = Interactive(objects[art_id])
        self.obj.draw_order = 1
        self.speed_mult = 1
        self.cheat_mult = 1
        self.points_add = 0
        if art_id == 0:
            self.speed_mult = 1.3
        elif art_id == 1:
            self.cheat_mult = 1.5
        elif art_id == 2:
            self.points_add = 150

    def change_stats(self, character):
        character.base_point_speed *= self.speed_mult
        character.speed *= self.speed_mult
        character.points += self.points_add

    def generate_pos(self, positions : pg.Vector2, offset : pg.Vector2, rd_box : pg.Vector2):
        ptr = rd.randint(0, len(positions) - 1)
        pos = pg.Vector2((rd.random()-0.5) * rd_box.x, (rd.random()-0.5) * rd_box.y)
        self.interactive.set_pos(positions[ptr] + pos + offset)

    def check_for_pickup(self, character):
        if self.interactive.near_character(character):
            if self.interactive.can_interact:
                self.change_stats(character)
                self.interactive.can_interact = False
                self.obj.visible = False



class Dialog:
    def __init__(self,actions ,maincards , testcards,positive_reactions, negative_reactions, right_answers, screen):
        self.number_of_maincard=0
        self.number_of_action=0
        self.number_of_test_card=0
        self.actions = actions
        self.testcards = testcards
        self.maincards = maincards
        self.positive_reactions = positive_reactions
        self.negative_reactions = negative_reactions
        self.right_answers = right_answers
        self.points=0
        self.screen = screen
        self.is_answered = False
        self.answer = False


    #Main phrases without variants of answers

    def main_talk(self):
        self.screen.blit(self.maincards[self.number_of_maincard], (0,0))
        if ovch_button.draw(self.screen):
            self.number_of_action+=1
            self.number_of_maincard+=1

    def test_talk(self):
        if not self.is_answered:
            self.screen.blit(self.testcards[self.number_of_test_card],(0,0))
            if a_button.draw(self.screen):
                self.is_answered=True
                if (self.right_answers[self.number_of_test_card] == 'A'):
                    self.answer = True
            if b_button.draw(self.screen):
                self.is_answered=True
                if (self.right_answers[self.number_of_test_card] == 'B'):
                    self.answer = True
            if c_button.draw(self.screen):
                self.is_answered=True
                if (self.right_answers[self.number_of_test_card] == 'C'):
                    self.answer = True
            if d_button.draw(self.screen):
                self.is_answered=True
                if (self.right_answers[self.number_of_test_card] == 'D'):
                    self.answer = True
        else:
            if (self.answer):
                self.screen.blit(self.positive_reactions[self.number_of_test_card], (0,0))
                if ovch_button.draw(self.screen):
                    self.number_of_action+=1
                    self.number_of_test_card+=1
                    self.points+=1
                    self.is_answered=False
                    self.answer=False
            else:
                self.screen.blit(self.negative_reactions[self.number_of_test_card], (0,0))
                if ovch_button.draw(self.screen):
                    self.number_of_action+=1
                    self.number_of_test_card+=1
                    self.is_answered=False
                    self.answer=False
                    self.points-=1
    def talk(self):
        if self.number_of_action<len(self.actions):
            if self.actions[self.number_of_action]=='M':
                self.main_talk()
            else:
                self.test_talk()
            return True
        else:
            return False













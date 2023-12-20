import pygame as pg
import math
import random as rd
import menu

WIDTH = 1280
HEIGHT = 720
teacher_waypoints = [pg.Vector2(400, 100), pg.Vector2(1000, 100),
                     pg.Vector2(400, 300), pg.Vector2(1000, 300),
                     pg.Vector2(400, 500), pg.Vector2(1000, 500)]

desks = [pg.Vector2(200 + i%3*300, 240 + int(i/3)*200) for i in range(9)]

chairs = [pg.Vector2(215 + i%2*80 + int(i/2)%3*300 + rd.random()*10, 260 + int(i/6)*200 + rd.random()*15) for i in range(18)]

buttons_height = HEIGHT*0.75+110
buttons_size = 0.75
a_button_img = pg.image.load("pictures/A_img.png")
b_button_img = pg.image.load("pictures/B_img.png")
c_button_img = pg.image.load("pictures/C_img.png")
d_button_img = pg.image.load("pictures/D_img.png")
ovch_button_img=pg.image.load("pictures/ovch_ok.png")
a_button = menu.Button(WIDTH/2+100, buttons_height, a_button_img, buttons_size)
b_button = menu.Button(WIDTH/2+200, buttons_height, b_button_img, buttons_size)
c_button = menu.Button(WIDTH/2+300, buttons_height, c_button_img, buttons_size)
d_button = menu.Button(WIDTH/2+400, buttons_height, d_button_img, buttons_size)
ovch_button = menu.Button(WIDTH/2+500, buttons_height, ovch_button_img, 0.5)

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

def intersects(r1, r2):
    """
    Args:
        r1(pg.Rect):
        r2(pg.Rect):

    Returns: Whether rectangles 1 and 2 intersect
    """
    flag = False
    if contains(r1, pg.Vector2(r2.x, r2.y)):
        flag = True
    elif contains(r1, pg.Vector2(r2.x + r2.width, r2.y)):
        flag = True
    elif contains(r1, pg.Vector2(r2.x, r2.y + r2.height)):
        flag = True
    elif contains(r1, pg.Vector2(r2.x, r2.y + r2.__contains__())):
        flag = True


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

        self.turn_speed = 10
        self.an = 0
        self.delta_an = 0
        self.target_an = 0
        self.waypoints = teacher_waypoints
        self.curr_target = pg.Vector2(self.obj.position.x, self.obj.position.y)
        self.vel_max = pg.Vector2(6, 6)
        self.max_sleepframes = 30
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
        self.scanpos = pg.Vector2(50, 20)
        self.sc_visible = Object(scanner.screen, scanner.images[0])
        self.dialogue = dialog
        self.look_angle = 90
        self.vision_range = 300

    def move(self):
        self.npc.move()
        self.sc_visible.images[0], new_rect = rotate(self.scanner.images[0], self.npc.an, self.npc.pos + self.scanpos, pg.Vector2(5, 120))
        self.sc_visible.position = new_rect

    def check(self, student):
        rel_pos = self.npc.pos + self.scanpos - pg.Vector2(student.position.x + student.position.width/2, student.position.y + student.position.height/2)
        rel_angle = math.atan2(rel_pos.y, rel_pos.x) * 180 / math.pi + 90
        if rel_angle < 0:
            rel_angle += 360
        return rel_pos.magnitude() < self.vision_range and is_close(rel_angle, self.npc.an, self.look_angle/2)

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
        if self.interactive.int_box.colliderect(character.position):
            character.near_student = True
            character.point_speed = character.base_point_speed * self.intellect * self.cooperation
            if not character.sitting:
                self.obj.anim_state = 1
            else:
                self.obj.anim_state = 0
        else:
            self.obj.anim_state = 0



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

    def interact(self, character, condition):
        '''
        interaction with the main character
        Args:
            character(Main_character):
            condition(bool):

        '''
        if self.int_box.colliderect(character.position) and self.can_interact:
            if not character.sitting:
                self.obj.anim_state = 1
            else:
                self.obj.anim_state = 0
            if condition and character.state_change_cooldown == 0:
                character.state_change_cooldown = 15
                if not character.sitting:
                    character.oldpos.x = character.position.x
                    character.oldpos.y = character.position.y
                    character.position.x = self.obj.position.x - 15
                    character.position.y = self.obj.position.y + 25
                    character.sitting = True
                    character.near_student = False
                    character.chair = self.obj
                else:
                    character.position.x = character.oldpos.x
                    character.position.y = character.oldpos.y
                    character.sitting = False
            elif character.state_change_cooldown > 0:
                character.state_change_cooldown -= 1
        else:
            self.obj.anim_state = 0




class Main_character:

    def __init__(self, screen: pg.Surface):

        self.speed = pg.Vector2(0, 0)
        self.image = pg.transform.scale(pg.image.load("pictures/hero.png"), (80, 100))
        self.position = self.image.get_rect(center = (100, 100))
        self.position.height =self.position.height/2
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
            if ((self.position.top < obj.position.bottom) and (self.position.bottom > obj.position.top) and (
                    self.position.left <= obj.position.right) and (self.position.left >= obj.position.centerx)):
                leftcrash = True
            if ((self.position.top < obj.position.bottom) and (self.position.bottom > obj.position.top) and (
                    self.position.right >= obj.position.left) and (self.position.right <= obj.position.centerx)):
                rightcrash = True
            if ((self.position.left < obj.position.right) and (self.position.right > obj.position.left) and (
                    self.position.top <= obj.position.bottom) and (self.position.top >= obj.position.centery)):
                topcrash = True
            if ((self.position.left < obj.position.right) and (self.position.right > obj.position.left) and (
                    self.position.bottom >= obj.position.top) and (self.position.bottom <= obj.position.centery)):
                bottomcrash = True

        return leftcrash, rightcrash, bottomcrash, topcrash

    def move(self, objects, Akey, Wkey, Skey, Dkey, Space):
        leftcrash = 0
        rightcrash = 0
        bottomcrash = 0
        topcrash = 0

        if not Space and not self.sitting:
            if (self.position.left <= 0):
                leftcrash = True
            if (self.position.right >= WIDTH):
                rightcrash = True
            if (self.position.top <= 150):
                topcrash = True
            if (self.position.bottom >= HEIGHT + 90):
                bottomcrash = True
            for obj in objects:
                if ((self.position.top < obj.position.bottom) and (self.position.bottom > obj.position.top) and (
                        self.position.left <= obj.position.right) and (self.position.left >= obj.position.centerx)):
                    leftcrash = True
                if ((self.position.top < obj.position.bottom) and (self.position.bottom > obj.position.top) and (
                        self.position.right >= obj.position.left) and (self.position.right <= obj.position.centerx)):
                    rightcrash = True
                if ((self.position.left < obj.position.right) and (self.position.right > obj.position.left) and (
                        self.position.top <= obj.position.bottom) and (self.position.top >= obj.position.centery)):
                    topcrash = True
                if ((self.position.left < obj.position.right) and (self.position.right > obj.position.left) and (
                        self.position.bottom >= obj.position.top) and (self.position.bottom <= obj.position.centery)):
                    bottomcrash = True

            if (Akey and not Dkey):
                if (leftcrash):
                    # self.position.x=self.position.x + self.speed.x
                    pass
                else:
                    self.position.x -= self.speed.x
            elif (Dkey and not Akey):
                if (rightcrash):
                    # self.position.x = self.position.x -  self.speed.x
                    pass
                else:
                    self.position.x += self.speed.x
            if (Wkey and not Skey):
                if (topcrash):
                    # self.position.y = self.position.y+self.speed.y
                    pass
                else:
                    self.position.y -= self.speed.y
            elif (Skey and not Wkey):
                if (bottomcrash):
                    # self.position.y = self.position.y-self.speed.y
                    pass
                else:
                    self.position.y += self.speed.y



    def draw(self):
        self.screen.blit(self.image, (self.position.x, self.position.y-self.position.height))


    def cheat(self, condition):
        '''
        Args:
            condition(bool): if conditions for cheating are met
        '''
        if(condition):
            self.points += self.point_speed

class Artefact(Object):
    pass

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
        if(ovch_button.draw(self.screen)):
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
                    self.is_answered=False
                    self.answer=False
            else:
                self.screen.blit(self.negative_reactions[self.number_of_test_card], (0,0))
                if ovch_button.draw(self.screen):
                    self.number_of_action+=1
                    self.number_of_test_card+=1
                    self.is_answered=False
                    self.answer=False
    def talk(self):
        if self.number_of_action<len(self.actions):
            if self.actions[self.number_of_action]=='M':
                self.main_talk()
            else:
                self.test_talk()
            return True
        else:
            return False













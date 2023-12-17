import pygame as pg
import math
import random as rd

WIDTH = 1280
HEIGHT = 720
teacher_waypoints = [pg.Vector2(400, 100), pg.Vector2(1000, 100),
                     pg.Vector2(400, 300), pg.Vector2(1000, 300),
                     pg.Vector2(400, 500), pg.Vector2(1000, 500)]

desks = [pg.Vector2(200 + i%3*300, 240 + int(i/3)*200) for i in range(9)]

chairs = [pg.Vector2(215 + i%2*80 + int(i/2)%3*300 + rd.random()*10, 280 + int(i/6)*200 + rd.random()*15) for i in range(18)]

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
        self.image = image
        self.position = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen = screen

        # TODO make images an array, add a variable for 'state' of the object, telling which image should be drawn
        #  we want to have animations later

    def draw(self):
        self.screen.blit(self.image, self.position)

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
        self.sc_visible = Object(scanner.screen, scanner.image)
        self.dialogue = dialog
        self.look_angle = 90
        self.vision_range = 300

    def move(self):
        self.npc.move()
        self.sc_visible.image, new_rect = rotate(self.scanner.image, self.npc.an, self.npc.pos + self.scanpos, pg.Vector2(5, 120))
        self.sc_visible.position = new_rect

    def check(self, student):
        rel_pos = self.npc.pos + self.scanpos - pg.Vector2(student.position.x + student.position.width/2, student.position.y + student.position.height/2)
        rel_angle = math.atan2(rel_pos.y, rel_pos.x) * 180 / math.pi + 90
        if rel_angle < 0:
            rel_angle += 360
        return rel_pos.magnitude() < self.vision_range and is_close(rel_angle, self.npc.an, self.look_angle/2)


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
        self.obj = object
        self.int_box = object.position


    def interact(self, character, condition):
        '''
        interaction with the main character
        Args:
            character(Main_character):
            condition(bool):

        '''
        if self.int_box.colliderect(character.position):
            if condition and character.state_change_cooldown == 0:
                character.state_change_cooldown = 30
                if not character.sitting:
                    character.oldpos.x = character.position.x
                    character.oldpos.y = character.position.y
                    character.position.x = self.obj.position.x - 15
                    character.position.y = self.obj.position.y + 25
                    character.sitting = True
                    character.chair = self.obj
                else:
                    character.position.x = character.oldpos.x
                    character.position.y = character.oldpos.y
                    character.sitting = False
            elif character.state_change_cooldown > 0:
                character.state_change_cooldown -= 1



class Main_character:

    def __init__(self, screen: pg.Surface):

        self.speed = pg.Vector2(0, 0)
        self.image = pg.transform.scale(pg.image.load("pictures/hero.png"), (80, 100))
        self.position = self.image.get_rect(center = (100, 100))
        self.position.height =self.position.height/2
        self.screen = screen
        self.points = 0
        self.point_speed = 1
        self.chance = 0

        self.sitting = False
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
            if (self.position.bottom >= HEIGHT):
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


    def cheat(self, Spacekey):
        if(Spacekey):
            self.points += self.point_speed


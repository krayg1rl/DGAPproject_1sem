import pygame as pg
import math
import random as rd

WIDTH = 1280
HEIGHT = 720
teacher_waypoints = [pg.Vector2(400, 100), pg.Vector2(1000, 100),
                     pg.Vector2(400, 300), pg.Vector2(1000, 300),
                     pg.Vector2(400, 500), pg.Vector2(1000, 500)]

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


class Object:
    def __init__(self, screen: pg.Surface, image):
        self.speed = pg.Vector2(0, 0)
        self.image = image
        self.position = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.position)


class NPC:
    def __init__(self, object, scanner):
        self.obj = object
        self.scanner = scanner
        self.sc_visible = Object(scanner.screen, scanner.image)

        self.pos = pg.Vector2(self.obj.position.x, self.obj.position.y)

        self.turn_speed = 5
        self.look_angle = 90
        self.an = 0
        self.delta_an = 0
        self.target_an = 0
        self.waypoints = teacher_waypoints
        self.curr_target = pg.Vector2(self.obj.position.x, self.obj.position.y)
        self.vel_max = pg.Vector2(3, 3)
        self.max_sleepframes = 30
        self.sleepframes = 0

    def new_target(self, target):
        self.curr_target = target
        self.sleepframes = self.max_sleepframes

    def look_around(self):
        pass

    def move(self):

        self.scanner.position.x = self.pos.x
        self.scanner.position.y = self.pos.y

        self.obj.position.x = self.pos.x
        self.obj.position.y = self.pos.y

        print(self.an, self.target_an)
        self.delta_an = 0
        if self.sleepframes == 0:
            if math.fabs(self.pos.x - self.curr_target.x) > 1.1 * self.vel_max.x:
                self.target_an = 180 + 90 * math.copysign(1, self.curr_target.x - self.pos.x)
                if math.fabs(self.an - self.target_an) < 4:
                    self.pos.x += math.copysign(self.vel_max.x, self.curr_target.x - self.pos.x)
                else:
                    self.an += self.turn_speed
                    self.delta_an = self.turn_speed
            elif math.fabs(self.pos.y - self.curr_target.y) > 1.1 * self.vel_max.y:
                self.target_an = 90 - 90 * math.copysign(1, self.curr_target.y - self.pos.y)
                if math.fabs(self.an - self.target_an) < 4:
                    self.pos.y += math.copysign(self.vel_max.y, self.curr_target.y - self.pos.y)
                else:
                    self.delta_an = self.turn_speed
                    self.an += self.turn_speed
            else:
                self.new_target(self.waypoints[rd.randint(0, len(self.waypoints) - 1)])
        else:
            self.sleepframes -= 1

        #self.sc_visible.image = pg.transform.rotate(self.scanner.image, self.an)
        self.sc_visible.image, new_rect = rotate(self.scanner.image, self.an, self.pos, pg.Vector2(0, 125))
        self.sc_visible.position = new_rect

        if self.an > 359:
            self.an -= 360


class Teacher:
    pass


class Main_character:

    def __init__(self, screen: pg.Surface):

        self.speed = pg.Vector2(0, 0)
        self.image = pg.transform.scale(pg.image.load("pictures/hero.png"), (80, 100))
        self.position = self.image.get_rect(center = (100, 100))
        self.position.height =self.position.height/2
        self.screen = screen
    def move(self, objects, Akey, Wkey, Skey, Dkey):
        leftcrash = 0
        rightcrash = 0
        bottomcrash = 0
        topcrash = 0
        if(self.position.left<=0):
            leftcrash=True
        if(self.position.right>=WIDTH):
            rightcrash = True
        if(self.position.top<=150):
            topcrash = True
        if(self.position.bottom>=HEIGHT):
            bottomcrash = True
        for obj in objects:
            if ((self.position.top< obj.position.bottom) and (self.position.bottom > obj.position.top) and(self.position.left<=obj.position.right) and (self.position.left>=obj.position.centerx)):
                leftcrash = True
            if ((self.position.top< obj.position.bottom) and (self.position.bottom > obj.position.top) and(self.position.right>=obj.position.left) and (self.position.right<=obj.position.centerx)):
                rightcrash = True
            if((self.position.left<obj.position.right) and (self.position.right>obj.position.left) and (self.position.top<=obj.position.bottom) and (self.position.top>=obj.position.centery)):
                topcrash = True
            if((self.position.left<obj.position.right) and (self.position.right>obj.position.left) and (self.position.bottom>=obj.position.top) and (self.position.bottom<=obj.position.centery)):
                bottomcrash = True

        if(Akey and not Dkey):
            if(leftcrash):
                #self.position.x=self.position.x + self.speed.x
                pass
            else:
                self.position.x-=self.speed.x
        elif(Dkey and not Akey):
            if(rightcrash):
                #self.position.x = self.position.x -  self.speed.x
                pass
            else:
                self.position.x+=self.speed.x
        if(Wkey and not Skey):
            if(topcrash):
                #self.position.y = self.position.y+self.speed.y
                pass
            else:
                self.position.y-=self.speed.y
        elif(Skey and not Wkey):
            if(bottomcrash):
                #self.position.y = self.position.y-self.speed.y
                pass
            else:
                self.position.y += self.speed.y



    def draw(self):
        self.screen.blit(self.image, (self.position.x, self.position.y-self.position.height))



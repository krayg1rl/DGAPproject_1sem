import pygame as pg
import math
import random as rd

WIDTH = 1280
HEIGHT = 720
teacher_waypoints = [pg.Vector2(400, 100), pg.Vector2(1000, 100),
                     pg.Vector2(400, 300), pg.Vector2(1000, 300),
                     pg.Vector2(400, 500), pg.Vector2(1000, 500)]
class Object:
    def __init__(self, screen: pg.Surface, image):

        self.speed = pg.Vector2(0, 0)
        self.image = image
        self.position = image.get_rect(center = (WIDTH/2, HEIGHT/2))
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.position)


class NPC:
    def __init__(self, object):
        self.obj = object

        self.scanner = 0
        self.turn_speed = 3
        self.look_angle = 90

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
        if self.sleepframes == 0:
            if (math.fabs(self.obj.position.x - self.curr_target.x) > 1.1*self.vel_max.x):
                self.obj.position.x += math.copysign(self.vel_max.x, self.curr_target.x - self.obj.position.x)
            elif (math.fabs(self.obj.position.y - self.curr_target.y) > 1.1*self.vel_max.y):
                self.obj.position.y += math.copysign(self.vel_max.y, self.curr_target.y - self.obj.position.y)
            else:
                self.new_target(self.waypoints[rd.randint(0, len(self.waypoints) - 1)])
        else:
            self.sleepframes -= 1


class Main_character:

    def __init__(self, screen: pg.Surface):

        self.speed = pg.Vector2(0, 0)
        self.image = pg.transform.scale(pg.image.load("pictures/prep1.png"), (80, 100))
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


#class Artefact

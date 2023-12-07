import pygame as pg
WIDTH = 1280
HEIGHT = 720
class Object:
    def __init__(self, screen: pg.Surface, image):

        self.speed = pg.Vector2(0, 0)
        self.image = image
        self.position = image.get_rect(center = (WIDTH/2, HEIGHT/2))
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.position)


class NPC(Object):
    def move(self):
        pass


class Main_character:

    def __init__(self, screen: pg.Surface, image):

        self.speed = pg.Vector2(0, 0)
        self.image = image
        self.position = image.get_rect(center = (100, 100))
        self.screen = screen
    def move(self, objects, Akey, Wkey, Skey, Dkey):
        leftcrash = 0
        rightcrash = 0
        bottomcrash = 0
        topcrash = 0
        for obj in objects:
            if ((self.position.top< obj.position.bottom) and (self.position.bottom > obj.position.top) and(self.position.left<obj.position.right) and (self.position.left>obj.position.centerx)):
                leftcrash = True
            if ((self.position.top< obj.position.bottom) and (self.position.bottom > obj.position.top) and(self.position.right>obj.position.left) and (self.position.right<obj.position.centerx)):
                rightcrash = True
            if((self.position.left<obj.position.right) and (self.position.right>obj.position.left) and (self.position.top< obj.position.bottom) and (self.position.top>obj.position.centery)):
                topcrash = True
            if((self.position.left<obj.position.right) and (self.position.right>obj.position.left) and (self.position.bottom> obj.position.top) and (self.position.bottom<obj.position.centery)):
                bottomcrash = True

        if(Akey and not Dkey):
            if(leftcrash):
                self.position.x=self.position.x + 2*self.speed.x
            else:
                self.position.x-=self.speed.x
        elif(Dkey and not Akey):
            if(rightcrash):
                self.position.x = self.position.x - 2 * self.speed.x
            else:
                self.position.x+=self.speed.x
        if(Wkey and not Skey):
            if(topcrash):
                self.position.y = self.position.y+2*self.speed.y
            else:
                self.position.y-=self.speed.y
        elif(Skey and not Wkey):
            if(bottomcrash):
                self.position.y = self.position.y-2*self.speed.y
            else:
                self.position.y += self.speed.y



    def draw(self):
        self.screen.blit(self.image, self.position)




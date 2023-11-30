import pygame as pg

class Object:
    def __init__(self):
        self.position = pg.Rect(0, 0, 0, 0)
        self.speed = pg.Vector2(0, 0)
        #self.image

    def draw(self):
        pass


class NPC(Object):
    def move(self):
        pass


class Main_character:

    def __init__(self):
        self.position = pg.Rect(0, 0, 0, 0)
        self.speed = pg.Vector2(0, 0)
        #self.image = pg

    def move(self, objects, Akey, Wkey, Skey, Dkey):
        pass








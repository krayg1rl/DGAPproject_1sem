"""
all drawing and displaying functions should be here
"""

window_width = 1280
window_height = 720

RED = (255, 0, 0)
BLACK = (0, 0, 0)

import pygame as pg
class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def update(self, drawables, screen):
        self.screen.fill(0, 0, 0)
        for drawable in drawables:
            drawable.draw(screen, self.center - pg.Vector2(window_width/2, window_height/2))

    def get_center(self, center):
        self.center = center

    def display(self):
        pg.display.update()

class Drawable:
    def __init__(self, obj):
        self.obj = obj
        self.drawable_type = 1 # we draw rectangles while sprites aren't ready
        self.visible = True




    def draw(self, surface, offset):
        if self.drawable_type == 0:
            pos = pg.Vector2(self.obj.position.x, self.obj.position.y)
            surface.blit(self.obj.sprite, pos + offset)
            #self.obj.draw(surface)
        elif self.drawable_type == 1:
            surface.draw.rect(surface, RED, self.obj.position)



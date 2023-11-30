"""
all drawing and displaying functions should be here
"""

RED = (255, 0, 0)
BLACK = (0, 0, 0)

import pygame as pg
class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def update(self, drawables, screen):
        self.screen.fill(0, 0, 0)
        for drawable in drawables:
            drawable.draw(screen)

    def display(self):
        pg.display.update()

class Drawable:
    def __init__(self, obj):
        self.obj = obj
        self.drawable_type = 1 # we draw rectangles while sprites aren't ready
        self.visible = True




    def draw(self, surface):
        if self.drawable_type == 0:
            #surface.blit(self.obj.sprite, self.pos)
            self.obj.draw(surface)
        elif self.drawable_type == 1:
            surface.draw.rect(surface, RED, self.obj.position)



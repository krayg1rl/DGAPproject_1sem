import pygame as pg


class Button:
    '''x and y are coordinates of center!!!'''
    def __init__(self, x, y, image, scale):
        image_width = image.get_width()
        image_height = image.get_height()
        self.image = pg.transform.scale(image, (int(image_width * scale), int(image_height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        self.is_mouse_over = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pg.mouse.get_pos()

        self.is_mouse_over = False

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if not self.is_mouse_over:
                surface.blit(self.image, (self.rect.x - 2, self.rect.y - 2))
                self.is_mouse_over = True
            if (pg.mouse.get_pressed()[0] == 1) and (self.clicked == False):
                self.clicked = True
                action = True
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen


        return action

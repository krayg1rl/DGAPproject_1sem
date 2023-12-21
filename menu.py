import pygame as pg


class Button:
    """
    Creates button given its image

        Args:
            x(float): x coordinate of center of floating window
            y(float): y coordinate of center of floating window
            image(pygame.Surface): image of button
            scale(float): size multiplication of image
    """
    def __init__(self, x, y, image, scale):
        image_width = image.get_width()
        image_height = image.get_height()
        self.image = pg.transform.scale(image, (int(image_width * scale), int(image_height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = True

    # draw button on screen
    def draw(self, surface):
        action = False
        # get mouse position
        pos = pg.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            surface.blit(self.image, (self.rect.x - 2, self.rect.y - 2))

            if (pg.mouse.get_pressed()[0] == 1) and (self.clicked == False):
                self.clicked = True
                action = True
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action


class FloatingWindow():
    """
    Creates floating window with text and buttons

        Args:
            window_x(float): x coordinate of top left corner of floating window
            window_y(float): y coordinate of top left corner of floating window
            window_image(pygame.Surface): image of floating window
            window_image_scale(float): size multiplication of window_image
            raw_buttons_information(list, tuple): information about buttons which will be placed on floating window
            ((button1_x, button1_y, button1_img, button1_scale), ...)
            button_x(float): x coordinate of top left corner of button
            button_y(float): y coordinate of top left corner of button
            button_image(pygame.Surface): image of button
            button_scale(float): size multiplication of button_image

    """

    def __init__(self, window_x, window_y, window_image, window_image_scale, raw_buttons_information):
        window_image_width = window_image.get_width()
        window_image_height = window_image.get_height()
        self.window_img = pg.transform.scale(window_image, (int(window_image_width * window_image_scale),
                                                            int(window_image_height * window_image_scale)))
        self.window_rect = self.window_img.get_rect()
        self.window_rect.topleft = (window_x, window_y)

        self.raw_buttons_information = raw_buttons_information
        self.buttons = []

        self.counter = 0
        self.transparency_change_time = 500  # in milliseconds
        self.transparency_change_step = 255 // (30 * self.transparency_change_time * 1e-3)
        self.alpha = 0  # transparency of window and buttons
        self.is_transparency_changing_ended = False

    def draw(self, surface):
        '''
        Function which draws window and buttons on it and returns number of button pressed
        :param surface:
        :return (str) number of button pressed starting from 0:
        '''

        if ((self.alpha == 255 and self.counter >= 30 * self.transparency_change_time * 1e-3)
                and self.is_transparency_changing_ended):
            self.counter = 0
            self.is_transparency_changing_ended = False

        for button in self.raw_buttons_information:
            self.buttons.append(Button(button[0], button[1], button[2], button[3]))

        if self.counter <= 30 * self.transparency_change_time * 1e-3:
            self.alpha = self.counter * self.transparency_change_step
            self.counter += 1

        if self.counter >= 30 * self.transparency_change_time * 1e-3:
            self.alpha = 255

        self.window_img.set_alpha(self.alpha)
        for button in self.buttons:
            button.image.set_alpha(self.alpha)

        surface.blit(self.window_img, (self.window_rect.x, self.window_rect.y))

        for button_number in range(len(self.buttons)):
            if self.buttons[button_number].draw(surface):
                self.is_transparency_changing_ended = True
                return str(button_number)


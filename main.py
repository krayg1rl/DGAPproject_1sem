"""
the main loop should be here
"""

import pygame
import numpy as np

FPS = 60

WIDTH = 1280
HEIGHT = 720

main_loop_running = True


'''Function which handle all events'''
def handle_envents(events):
    global main_loop_running

    '''dict with key names and bool value which indicates whether key is pressed or not
    <key_name>: <pressed_or_not>'''
    keys_pressed = {'SPACE': False}  # SPACE key here is for example

    for event in events:
        if event.type == pygame.QUIT:
            main_loop_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                keys_pressed['SPACE'] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                keys_pressed['SPACE'] = False

    if keys_pressed['SPACE']:
        pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    while main_loop_running:
        clock.tick(FPS)

        handle_envents(pygame.event.get())


if __name__ == "__main__":
    main()
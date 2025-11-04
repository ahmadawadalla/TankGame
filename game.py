import time

import pygame
from gameWorld import GameWorld

if __name__ == '__main__':
    pygame.init()
    WIDTH = 1000
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("TankGame")

    gw = GameWorld(screen)
    gw.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # list of all the keys pressed
        keys = pygame.key.get_pressed()

        # list of all the mouse buttons pressed
        mouse_buttons = pygame.mouse.get_pressed()

        if gw.check_win() == 0:
            gw.mouse_button_pressed(mouse_buttons)
            gw.tank_moves(keys)
        else:
            if gw.check_replay(mouse_buttons):
                time.sleep(0.2)
                screen = pygame.display.set_mode((WIDTH,HEIGHT))
                pygame.display.set_caption("TankGame")
                gw = GameWorld(screen)
                gw.update()


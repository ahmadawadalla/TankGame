import pygame
from gameWorld import GameWorld

if __name__ == '__main__':
    pygame.init()
    WIDTH = 1000
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("TankGame")

    gw = GameWorld(screen)
    gw.draw()
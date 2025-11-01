import pygame

class Grenade:
    def __init__(self,screen):
        self.screen = screen
        self.damage = 10
        self.radius = 7 # how big the projectile is
        self.blast_radius = 45
        self.name = 'Grenade'

    def draw(self,x,y):
        black = (0,0,0)
        pygame.draw.circle(self.screen,black,(x,y),self.radius)
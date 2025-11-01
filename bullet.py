import pygame

class Bullet:
    def __init__(self,screen):
        self.screen = screen
        self.damage = 20
        self.radius = 5 # how big the projectile is
        self.blast_radius = 30
        self.name = 'Bullet'

    def draw(self,x,y):
        black = (0,0,0)
        pygame.draw.circle(self.screen,black,(x,y),self.radius)
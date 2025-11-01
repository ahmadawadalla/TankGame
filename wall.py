import pygame

class Wall:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        black = (0,0,0)
        x = self.screen.get_width()//2 - 20
        y = 200
        pygame.draw.rect(self.screen,black,(x,y,50,self.screen.get_height() - y))
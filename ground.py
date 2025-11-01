import random
import numpy as np
import pygame.draw


def make_grid(screen):
    # base_ground is the smallest y level for the ground
    screen_w = screen.get_width()
    screen_h = screen.get_height()
    base_ground = screen_h//3
    ground_width = screen_w / 2 - 25

    plots = []

    rng1 = random.randint(base_ground//2,1/2 * screen.get_height())
    rng2 = random.randint(base_ground//2,1/2 * screen.get_height())

    rng3 = random.randint(base_ground//2,1/2 * screen.get_height())
    rng4 = random.randint(base_ground//2,1/2 * screen.get_height())

    num = 100

    plot1 = (0, base_ground)
    plot2 = (1 / 4 * ground_width, base_ground)
    plot3 = (2 / 4 * ground_width, rng1)
    plot4 = (3 / 4 * ground_width, rng1)
    plot5 = (ground_width, rng2)

    plot6 = (screen_w, base_ground)
    plot7 = (screen_w - 1 / 4 * ground_width, base_ground)
    plot8 = (screen_w - 2 / 4 * ground_width, rng3)
    plot9 = (screen_w - 3 / 4 * ground_width, rng3)
    plot10 = (screen_w - ground_width, rng4)

    x = np.linspace(plot1[0],plot2[0],num)
    x = np.append(x, np.linspace(plot2[0],plot3[0],num))
    x = np.append(x, np.linspace(plot3[0],plot4[0],num))
    x = np.append(x, np.linspace(plot4[0],plot5[0],num))

    x = np.append(x, np.linspace(plot10[0],plot9[0],num))
    x = np.append(x, np.linspace(plot9[0],plot8[0],num))
    x = np.append(x, np.linspace(plot8[0],plot7[0],num))
    x = np.append(x, np.linspace(plot7[0],plot6[0],num))

    y = np.linspace(plot1[1],plot2[1],num)
    y = np.append(y, np.linspace(plot2[1],plot3[1],num))
    y = np.append(y, np.linspace(plot3[1],plot4[1],num))
    y = np.append(y, np.linspace(plot4[1],plot5[1],num))

    y = np.append(y, np.linspace(plot10[1],plot9[1],num))
    y = np.append(y, np.linspace(plot9[1],plot8[1],num))
    y = np.append(y, np.linspace(plot8[1],plot7[1],num))
    y = np.append(y, np.linspace(plot7[1],plot6[1],num))
    return x,y

class Ground:
    def __init__(self, screen):
        self.screen = screen
        self.ground_grid = make_grid(screen)
        self.color = (0,255,0)


    def draw(self):
        x,y = self.ground_grid
        for i in range(len(x)):
            pygame.draw.rect(self.screen,self.color,(x[i],y[i]+250,5,600 - y[i]))
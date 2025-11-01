import math
import time

from tank import Tank
from ground import Ground
from wall import Wall
from projectiles import Projectiles
import pygame

class GameWorld:
    def __init__(self,screen):
        self.screen = screen

        # player 1
        self.tank1 = Tank(self.screen,1)
        # player 2
        self.tank2 = Tank(self.screen,2)

        # determines which tanks turn it is
        self.curr_tank = self.tank1

        self.ground = Ground(self.screen)

        self.wall = Wall(screen)

        self.projectiles = Projectiles(screen)

        self.projectile_index = 0 # indicates which projectile
        self.projectile_time = 0 # the time since it was fired
        self.projectile_speed = 50 # max speed is 100

        self.impact_list = [] # contains a list of white circle to be displayed on the screen

        self.mouse_button_time = 0 # the lat time I pressed the mouse_button

        # even move is player 1, odd is player 2
        self.move_number = 0

    def update(self):
        self.update_wo_flip()
        pygame.display.flip()

    def update_wo_flip(self):
        self.screen.fill('white')
        self.ground.draw()
        self.draw_impacts()
        self.tank1.draw()
        self.tank2.draw()
        self.wall.draw()

        self.draw_header()

    def blast_hit(self,projectile,xi,yi):
        # xi, yi = blast coordinate
        x1,y1 = self.tank1.position
        x2,y2 = self.tank2.position

        x1 += self.tank1.width / 2
        y1 += self.tank1.height / 2

        x2 += self.tank1.width / 2
        y2 += self.tank1.height / 2

        d1 = math.sqrt((x1 - xi) ** 2 + (y1 - yi) ** 2)
        d2 = math.sqrt((x2 - xi) ** 2 + (y2 - yi) ** 2)

        if d1 <= projectile.blast_radius:
            self.tank1.hp -= projectile.damage
            if self.tank1.hp < 0:
                self.tank1.hp = 0
        if d2 <= projectile.blast_radius:
            self.tank2.hp -= projectile.damage
            if self.tank2.hp < 0:
                self.tank2.hp = 0

    def update_projectile(self):
        black = (0,0,0,255)
        green = (0,255,0,255)

        projectile = self.projectiles.projectile_list[self.projectile_index]

        x0,y0 = self.curr_tank.turret_pos

        x = x0
        y = y0

        while self.screen.get_width() - projectile.radius > x > 0 and y < self.screen.get_height() - projectile.radius:
            if y > 0:
                impact_color = self.screen.get_at((x + projectile.radius,y + projectile.radius))
                turret_x,turret_y = self.curr_tank.turret_pos
                d = math.sqrt((x - turret_x) ** 2 + (y - turret_y) ** 2)

                if impact_color in [green, black] and d > 10:
                    self.impact_list.append((projectile,x,y))
                    self.update()
                    break

            # every 10 pixels is 1 meter
            speed = self.projectile_speed * 3.5
            angle = self.curr_tank.aim_angle + self.curr_tank.angle
            t = (time.time() - self.projectile_time) * 2
            g = 98.1

            x = int(x0 + speed * math.cos(math.radians(angle)) * t)
            y = int(- 1/2 * g * t ** 2 + speed * math.sin(math.radians(angle)) * t)
            y = y0 - y

            self.update_wo_flip()
            projectile.draw(x,y)
            pygame.display.flip()

        self.blast_hit(projectile,x,y)
        self.update()

    def tank_moves(self,keys):
        # if d is being held down, then move right
        if keys[pygame.K_d]:
            self.curr_tank.move_tank('right')
            self.update()

        # if a is being held down, then move left
        if keys[pygame.K_a]:
            self.curr_tank.move_tank('left')
            self.update()

        # if the left arrow is being held down the change the angle of the turret
        if keys[pygame.K_LEFT]:
            self.curr_tank.change_aim_angle('left')
            self.update()

        # if the right arrow is being held down the change the angle of the turret
        if keys[pygame.K_RIGHT]:
            self.curr_tank.change_aim_angle('right')
            self.update()

        # if the space bar is pressed, then fire the turret
        if keys[pygame.K_SPACE]:
            self.projectile_time = time.time() # update initial time shot
            self.update_projectile()
            self.move_number += 1

            self.curr_tank = self.tank1 if self.move_number % 2 == 0 else self.tank2
            time.sleep(0.25)
            self.update()

    def mouse_button_pressed(self,mouse_buttons):
        x,y = pygame.mouse.get_pos()

        if mouse_buttons[0]:
            if time.time() - self.mouse_button_time > 0.05: # power
                if 108 >= x >= 83 and 78 >= y >= 53: # left arrow has been clicked
                    self.projectile_speed -= 1
                    self.update()
                    self.mouse_button_time = time.time()

                elif 183 >= x >= 158 and 78 >= y >= 53: # right arrow has been clicked
                    self.projectile_speed += 1
                    self.update()
                    self.mouse_button_time = time.time()

            if time.time() - self.mouse_button_time > 0.025: # angle
                if 228 >= x >= 203 and 78 >= y >= 53: # left arrow has been clicked
                    self.curr_tank.aim_angle -= 1
                    self.update()
                    self.mouse_button_time = time.time()

                elif 302 >= x >= 277 and 78 >= y >= 53: # right arrow has been clicked
                    self.curr_tank.aim_angle += 1
                    self.update()
                    self.mouse_button_time = time.time()

            if time.time() - self.mouse_button_time > .15: # weapons dropdown
                if 602 >= x >= 577 and 51 >= y >= 40: # up arrow has been clicked
                    self.projectile_index = (self.projectile_index + 1) % len(self.projectiles.projectile_list)
                    self.update()
                    self.mouse_button_time = time.time()

                elif 602 >= x >= 577 and 64 >= y >= 53: # down arrow has been clicked
                    self.projectile_index = (self.projectile_index - 1) % len(self.projectiles.projectile_list)
                    self.update()
                    self.mouse_button_time = time.time()

    def draw(self):
        self.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # list of all the keys pressed
            keys = pygame.key.get_pressed()
            self.tank_moves(keys)

            # list of all the mouse buttons pressed
            mouse_buttons = pygame.mouse.get_pressed()
            self.mouse_button_pressed(mouse_buttons)

    def draw_header(self):
        self.draw_slider()
        self.show_angle()
        self.draw_weapon_dropdown()

        self.draw_hp_bar()

    def draw_slider(self):
        x0,y0 = 10,10

        slider_width = 175
        slider_height = 70

        if self.projectile_speed > 100:
            self.projectile_speed = 100
        elif self.projectile_speed < 1:
            self.projectile_speed = 1

        background = (150,150,150)
        white = (255,255,255)
        black = (40,40,40)
        red = (225,0,0)

        # slider background
        black_background = pygame.draw.rect(self.screen,black,(x0,y0,slider_width,slider_height),0,20,border_bottom_right_radius=0)
        top_rect = pygame.draw.rect(self.screen,background,(x0,y0,slider_width,slider_height - 30),10,0,7,7)
        bottom_left_rect = pygame.draw.rect(self.screen,background,(x0,y0 + top_rect.height,2/5 * slider_width,slider_height - 40),0,7,0,0)

        #buttons
        self.draw_left_arrow(83,53,background)
        self.draw_right_arrow(slider_width - 17,53,background)

        # slider power level
        power_slider = pygame.draw.rect(self.screen,red,(x0 + 15,y0 + 15,(self.projectile_speed / 100) * (slider_width - 30),10),0,2)

        # power text
        self.draw_text(x0 + 7,y0 + 40,-7,'Power')
        self.draw_text(x0 + 10,y0 + 45,-1.7,'Power',24,white)

        # power number
        self.draw_numbers(slider_width - 65,53,47,25,self.projectile_speed)

    def show_angle(self):
        x0 = 200
        y0 = 10

        width,height = 105,40

        if self.curr_tank.aim_angle < 0:
            self.curr_tank.aim_angle = 0
        elif self.curr_tank.aim_angle > 180:
            self.curr_tank.aim_angle = 180

        background = (150,150,150)
        white = (255,255,255)
        black = (40,40,40)

        pygame.draw.rect(self.screen,background,(x0,y0,width,height),0,0,25,25)
        pygame.draw.rect(self.screen,black,(x0,y0+ height,width,30))

        # buttons
        self.draw_left_arrow(x0 + 3,y0+height + 3,background)
        self.draw_right_arrow(x0 + width - 28,y0+height + 3,background)

        # angle text
        self.draw_text(x0+24,y0+8,-5,'Anole',35)
        self.draw_text(x0+28,y0+13,0.4,'Angle',22,white)

        # angle number
        self.draw_numbers(x0+30,y0+43,46,25,self.curr_tank.aim_angle)

    def draw_weapon_dropdown(self):
        x0,y0 = 320,25

        width = 200
        height = 55

        background = (150,150,150)
        white = (255,255,255)
        black = (40,40,40)

        projectile_name = self.projectiles.projectile_list[self.projectile_index].name

        weapons_dropdown = pygame.draw.rect(self.screen,background,(x0,y0,90,height),0,0,5,0,5)

        self.draw_text(x0 + 8,y0 + 17,-4.9,'Weapon',31)
        self.draw_text(x0 + 10.5,y0 + 20,0,'Weapon',23,white)

        # projectile background
        black_background = pygame.draw.rect(self.screen,black,(x0 + weapons_dropdown.width,y0,width,height),0,10,0,10,0)
        weapon_rect = pygame.draw.rect(self.screen,background,(x0 + weapons_dropdown.width,y0,width,height),13,10,0,10,0)

        # projectile text
        self.draw_text(x0 + 106,y0 + 18,0,projectile_name,30,white,False)

        # buttons
        self.draw_right_arrow(x0 + weapon_rect.width + weapons_dropdown.width - 33,y0 + 15,background,25,22,90,0.75,0.5)
        self.draw_left_arrow(x0 + weapon_rect.width + weapons_dropdown.width - 33,y0 + 28,background,25,22,90,0.75,0.5)

    def draw_hp_bar(self):
        x0,y0 = 750,40

        width = 175
        height = 40

        background = (150,150,150)
        white = (255,255,255)
        black = (40,40,40)
        red = (225,0,0)

        # hp text

        hp_rect = pygame.draw.rect(self.screen,background,(x0,y0,40,height),0,0,5,0,5)

        self.draw_text(x0 + 15,y0 + 8,-4,'hp',33)
        self.draw_text(x0 + 17.5,y0 + 12,-.1,'hp',22,white)

        # hp background
        black_background = pygame.draw.rect(self.screen,black,(x0 + hp_rect.width,y0,width,height),0,10,0,10,0)
        hp_bar = pygame.draw.rect(self.screen,background,(x0 + hp_rect.width,y0,width,height),13,10,0,10,0)

        # slider power level
        health_level = pygame.draw.rect(self.screen,red,(x0 + hp_rect.width + 15,y0 + 15,(self.curr_tank.hp / 100) * (width - 30),10),0,2)

    def draw_left_arrow(self,x,y,background=(255,255,255),width=25,height=25,angle=0, scale_width=1,scale_height=1):
        left_arrow = pygame.image.load('Images/arrow.png')
        left_arrow = pygame.transform.rotate(left_arrow,angle)

        width,height = left_arrow.get_size()
        width = int(width * scale_width)
        height = int(height * scale_height)

        left_arrow = pygame.transform.scale(left_arrow,(width,height))
        left_button = pygame.draw.rect(self.screen,background,(x,y,width,height))
        self.screen.blit(left_arrow,left_button)

    def draw_right_arrow(self,x,y,background=(255,255,255),width=25,height=25,angle=0,scale_width=1,scale_height=1):
        self.draw_left_arrow(x,y,background,width,height,angle + 180,scale_width,scale_height)

    def draw_text(self,x,y,letter_spacing,text,size=35,color=(40,40,40),is_bold=True):
        font = pygame.font.SysFont('Comforta',size)
        font.set_bold(is_bold)

        for char in text:
            char_surface = font.render(char, True, color)
            self.screen.blit(char_surface, (x, y))
            x += char_surface.get_width() + letter_spacing

    def draw_numbers(self,x,y,width,height,number,bg_color = (40,40,40),color = (255,255,255)):
        font = pygame.font.SysFont('Arial',25)

        number_box = pygame.draw.rect(self.screen,bg_color,(x,y,width,height))
        number_text = font.render(str(number),True,color)

        if len(str(number)) == 1: # 1 digit
            dx = 16
        elif len(str(number)) == 2: # 2 digits
            dx = 9
        else: # 3 digits
            dx = 1

        self.screen.blit(number_text,(number_box.x + dx,number_box.y-1))

    def draw_impacts(self):
        white = (255,255,255)
        for i in self.impact_list:
            projectile,x,y = i
            pygame.draw.circle(self.screen,white,(x,y),projectile.blast_radius)
import math
import time
import pygame

class Tank:
    def __init__(self, screen, id):
        self.hp = 100
        self.id = id
        self.aim_angle = 0 # the initial aim angle is 0 degrees (can be between 0-180)
        self.angle = 0 # the tank is initially flat on the surface (0 degrees)
        self.power = 10 # the initial power is 10 (max power is 10)
        self.screen = screen

        self.aim_angle_time = time.time() # the last time you changed the angle
        self.move_tank_time = time.time() # the last time you moved the tank

        self.turret_pos = (70,485) # gets the position of the tip of the turret
        self.width = 0
        self.height = 0

        if id == 1:
            self.position = (0,454) # player 1's initial position
            self.color = (0,185,0)

        else:
            self.position = (940,454) # player 2's initial position
            self.color = (185,0,0)
            self.aim_angle = 180

    def change_aim_angle(self,direction):
        # direction can be 'left' or 'right'
        if time.time() - self.aim_angle_time < 0.01:
            return

        angle = self.aim_angle + 1 if direction == 'left' else self.aim_angle - 1
        self.aim_angle = angle if 180 >= angle >= 0 else self.aim_angle
        self.aim_angle_time = time.time()

    def move_tank(self, direction):
        if time.time() - self.move_tank_time < 0.03:
            return

        def is_ground(px, py):
            return self.screen.get_at((px, py)) == green

        def is_wall(px, py):
            return self.screen.get_at((px, py)) == black

        black = (0,0,0,255)
        green = (0,255,0,255)
        speed = 2

        x = self.position[0] + (speed if direction == 'right' else -speed)
        x = max(0, min(940, x))
        y = self.position[1]

        if self.id == 1: # if player 1
            if is_wall(x + 70,y):
                return
        else: # if player 2
            if is_wall(x - 2,y):
                return

        TRACK_OFFSET_Y = 60
        WHEELBASE_X    = 58

        screen_w, screen_h = self.screen.get_width(), self.screen.get_height()

        def surface_y_at(px, start_y):
            # Find the top edge of ground at column px, starting near the track line.
            px = max(0, min(screen_w - 1, px))
            y0 = max(0, min(screen_h - 1, int(start_y)))

            # If we're in the air, go DOWN to hit ground
            if not is_ground(px, y0):
                y1 = y0
                while y1 < screen_h - 1 and not is_ground(px, y1):
                    y1 += 1
            else:
                y1 = y0

            # Now walk UP to the top edge of ground
            while y1 > 0 and is_ground(px, y1 - 1):
                y1 -= 1
            return y1

        # Probe columns for rear/front tracks
        rear_x  = int(max(0, min(screen_w - 1, x)))
        front_x = int(max(0, min(screen_w - 1, x + WHEELBASE_X)))
        track_y = int(min(screen_h - 1, y + TRACK_OFFSET_Y))

        # Small 3px horizontal average to smooth noisy edges
        rear_y  = (surface_y_at(rear_x - 1, track_y) +
                   surface_y_at(rear_x, track_y) +
                   surface_y_at(rear_x + 1, track_y)) // 3

        front_y = (surface_y_at(front_x - 1, track_y) +
                   surface_y_at(front_x, track_y) +
                   surface_y_at(front_x + 1, track_y)) // 3

        # Tilt from slope (screen y grows downward)
        dy = front_y - rear_y
        dx = float(WHEELBASE_X)
        theta = math.atan2(-dy, dx)
        self.angle = math.degrees(theta)

        # Place hull so the higher track touches the ground
        y = min(rear_y, front_y) - TRACK_OFFSET_Y - 2
        y -= int(26 * self.angle/90)

        self.position = (x, y)
        self.move_tank_time = time.time()

    def draw(self):
        x,y = self.position # the tanks position on the map

        # first player is green second player is red
        red = (255,0,0,255)

        # dimensions
        body_width, body_height = 60, 25
        hatch_width, hatch_height = 35, 20
        turret_width, turret_height = 22, 8

        # using surface for tilting the tank at an angle
        tank_surface = pygame.Surface((body_width,body_height + hatch_height + turret_width - 5),pygame.SRCALPHA)
        turret_surface = pygame.Surface((turret_width*2.5,turret_height),pygame.SRCALPHA)

        # body
        body = pygame.draw.rect(tank_surface, self.color, (0,tank_surface.get_height() - body_height ,body_width,body_height),
                                border_top_left_radius=5, border_top_right_radius=5,
                                border_bottom_left_radius=10, border_bottom_right_radius=10)

        self.draw_rect_border(tank_surface,body,5,5,5,10,10)

        # hatch
        hatch = pygame.draw.rect(tank_surface, self.color,(tank_surface.get_width()/5,tank_surface.get_height() - body_height - hatch_height + 5,hatch_width,hatch_height),
                                 border_top_left_radius=10, border_top_right_radius=10)

        self.draw_rect_border(tank_surface,hatch, 5,10,10)

        # turret
        turret = pygame.draw.rect(turret_surface, self.color, (1.6*turret_surface.get_width()/2.5,0,turret_width,turret_height))
        self.draw_rect_border(turret_surface,turret,3)

        pygame.draw.rect(turret_surface,red,(1.6*turret_surface.get_width()/2.5 + turret_width -5,0,5,turret_height))

        # tilting the turret
        rotated_turret = pygame.transform.rotate(turret_surface,self.aim_angle)

        tank_surface.blit(rotated_turret, rotated_turret.get_rect(center=hatch.center).topleft)

        tank = pygame.transform.rotate(tank_surface,self.angle)

        self.screen.blit(tank,(x,y))

        for tank_x in range(x, x + tank_surface.get_width()):
            for tank_y in range(y, y + tank_surface.get_height()):
                if self.screen.get_at((tank_x,tank_y)) == red:
                    self.turret_pos = (tank_x,tank_y - 3)
                    break

        self.width = tank.get_width()
        self.height = tank.get_height()

    def draw_rect_border(self,surface, rect, width=0, top_left=0,top_right=0,bottom_left=0,bottom_right=0):
        pygame.draw.rect(surface,(0,0,0),(rect.x,rect.y,rect.width, rect.height),
                         width,0,top_left,top_right,bottom_left,bottom_right)

from bullet import Bullet
from grenade import Grenade

class Projectiles:
    def __init__(self,screen):
        self.screen = screen
        self.projectile_list = []

        self.projectile_list.append(Bullet(screen))
        self.projectile_list.append(Grenade(screen))


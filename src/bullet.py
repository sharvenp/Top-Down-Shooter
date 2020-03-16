
from utils import Utils
from settings import Settings
from projectile import Projectile
from collideable import Collideable

import pygame as pg

class Bullet(Projectile, Collideable):

    def __init__(self, position, direction, speed, color):
        Projectile.__init__(self, 1, position, direction)
        Collideable.__init__(self, Settings.BULLET_SIZE)
        self.speed = speed
        self.color = color

    def step(self):
        nx, ny = Utils.direction_position(self.position, self.rotation, self.speed * Settings.DELTA_TIME)

        if not ((0 <= nx <= Settings.WIDTH) and (0 <= ny <= Settings.HEIGHT)):
            self.destroyed = True

        self.position = (nx, ny)

    def render(self, screen):
        pg.draw.circle(screen, self.color, self.position, Settings.BULLET_SIZE)

    def on_collide(self, other):
        self.destroyed = True

        # Deal damage
        other.deal_damage(Settings.PLAYER_DAMAGE)
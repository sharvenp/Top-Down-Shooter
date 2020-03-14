
from utils import Utils
from settings import Settings
from projectile import Projectile

import pygame as pg

class Bullet(Projectile):

    def __init__(self, position, direction, speed, color):
        Projectile.__init__(self)
        self.position = position
        self.direction = direction
        self.speed = speed

        self.color = color

    def step(self):
        nx, ny = Utils.direction_position(self.position, self.direction, self.speed * Settings.DELTA_TIME)

        if not ((0 <= nx <= Settings.WIDTH) and (0 <= ny <= Settings.HEIGHT)):
            self.destroyed = True

        self.position = (nx, ny)

    def render(self, screen):
        pg.draw.circle(screen, self.color, self.position, Settings.BULLET_SIZE)
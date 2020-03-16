
from controllable import Controllable
from bullet import Bullet
from collideable import Collideable
from health import Health
from utils import Utils
from settings import Settings

import pygame as pg

class Player(Controllable, Collideable, Health):

    def __init__(self, position):
        Controllable.__init__(self, 0, position, 0)
        Collideable.__init__(self, Settings.PLAYER_SIZE)
        Health.__init__(self, Settings.PLAYER_HEALTH)
        self.score = 0

    def move(self, direction):

        if Settings.DEBUG:
            print(f"Moving Player")

        nx, ny = Utils.direction_position(self.position, self.rotation, direction * Settings.PLAYER_MOVEMENT_SPEED * Settings.DELTA_TIME)

        if not ((0 <= nx <= Settings.WIDTH) and (0 <= ny <= Settings.HEIGHT)):
            if Settings.DEBUG:
                print("Reached Bounds")
            return

        self.position = (nx, ny)

    def turn(self):

        mpos = pg.mouse.get_pos()
        angle = Utils.get_look_angle(self.position, mpos)
        self.rotation = angle % 360

        if Settings.DEBUG:
            print(f"New Player Angle: {self.rotation}")

    def shoot(self):

        if Settings.DEBUG:
            print("Player Shooting")
        
        nx, ny = Utils.direction_position(self.position, self.rotation, Settings.SHOOT_START_DIST)
        bullet = Bullet((nx, ny), self.rotation, Settings.BULLET_SPEED, Settings.BULLET_COLOR_PLAYER)
        return bullet


    def render(self, screen):
        pg.draw.circle(screen, Settings.PLAYER_COLOR, self.position, Settings.PLAYER_SIZE)

        nx, ny = Utils.direction_position(self.position, self.rotation, Settings.SHOOT_START_DIST)
        pg.draw.line(screen, Settings.PLAYER_COLOR, self.position, (nx, ny), 3)

    def on_collide(self, other):
        pass
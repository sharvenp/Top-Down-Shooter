
from controllable import Controllable
from settings import Settings
from bullet import Bullet
from utils import Utils

import pygame as pg

class Player(Controllable):

    def __init__(self, position):
        Controllable.__init__(self)
        self.position = position
        self.look_angle = 0
        
    def move(self, direction):

        if Settings.DEBUG:
            print(f"Moving Player")

        nx, ny = Utils.direction_position(self.position, self.look_angle, direction * Settings.PLAYER_MOVEMENT_SPEED * Settings.DELTA_TIME)

        if not ((0 <= nx <= Settings.WIDTH) and (0 <= ny <= Settings.HEIGHT)):
            if Settings.DEBUG:
                print("Reached Bounds")
            return

        self.position = (nx, ny)

    def turn(self):

        mpos = pg.mouse.get_pos()
        angle = Utils.get_look_angle(self.position, mpos)
        self.look_angle = angle % 360

        if Settings.DEBUG:
            print(f"New Player Angle: {self.look_angle}")

    def shoot(self):

        if Settings.DEBUG:
            print("Player Shooting")
        
        nx, ny = Utils.direction_position(self.position, self.look_angle, Settings.SHOOT_START_DIST)
        bullet = Bullet((nx, ny), self.look_angle, Settings.BULLET_SPEED, Settings.BULLET_COLOR_PLAYER)
        return bullet


    def render(self, screen):
        pg.draw.circle(screen, Settings.PLAYER_COLOR, self.position, Settings.PLAYER_SIZE)

        nx, ny = Utils.direction_position(self.position, self.look_angle, Settings.SHOOT_START_DIST)
        pg.draw.line(screen, (0, 255, 0), self.position, (nx, ny), 3)
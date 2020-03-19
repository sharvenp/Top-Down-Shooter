
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
        self.ray_data = []

    def reset(self, position):
        self.destroyed = False
        self.health = Settings.PLAYER_HEALTH
        self.position = position
        self.rotation = 0
        self.ray_data = []

    def move(self, direction):

        if Settings.DEBUG:
            print(f"Moving Player")

        nx, ny = Utils.direction_position(self.position, self.rotation, direction * Settings.PLAYER_MOVEMENT_SPEED * Settings.DELTA_TIME)

        if not ((0 <= nx <= Settings.WIDTH) and (0 <= ny <= Settings.HEIGHT)):
            if Settings.DEBUG:
                print("Reached Bounds")
            return

        self.position = (nx, ny)

    def turn(self, angle):

        self.rotation = angle

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

        if Settings.AGENT_DEBUG and self.ray_data:
            for ray in self.ray_data:
                blocks, hit_type = ray
                for block in blocks:
                    bx, by = block
                    c = (255, 0, 255)
                    if hit_type:
                        c = (255, 255, 255)
                    pg.draw.rect(screen, c, (bx, by, 1, 1)) 

            pg.draw.circle(screen, (0, 255, 0), self.position, Settings.AWARENESS_RANGE, 1)

    def on_collide(self, other):
        pass
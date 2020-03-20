
from controllable import Controllable
from collideable import Collideable
from health import Health
from utils import Utils
from settings import Settings

import pygame as pg

class Enemy(Controllable, Collideable, Health):

    def __init__(self, position, players):
        Controllable.__init__(self, 2, position, 0)
        Collideable.__init__(self, Settings.ENEMY_SIZE)
        Health.__init__(self, Settings.ENEMY_HEALTH)
        self.players = players

        self.min_distance = Settings.ENEMY_SIZE + Settings.ENEMY_MIN_DISTANCE

    def move(self):
        d = float('inf')
        closest_player = None
        for player in self.players:
            dist = Utils.get_distance(self.position, player.position)
            if dist < d:
                d = dist
                closest_player = player
        if d > self.min_distance:
            self.position = Utils.direction_position(self.position, self.rotation, Settings.ENEMY_MOVEMENT_SPEED * Settings.DELTA_TIME)
        else:
            # Deal Damage
            closest_player.deal_damage(Settings.ENEMY_DAMAGE)

    def turn(self):

        d = float('inf')
        closest_player = None
        for player in self.players:
            dist = Utils.get_distance(self.position, player.position)
            if dist < d:
                d = dist
                closest_player = player

        angle = Utils.get_look_angle(self.position, closest_player.position)
        self.rotation = angle % 360

    def render(self, screen):
        pg.draw.circle(screen, Settings.ENEMY_COLOR, self.position, Settings.ENEMY_SIZE)

        nx, ny = Utils.direction_position(self.position, self.rotation, 8)
        pg.draw.line(screen, (255, 0, 0), self.position, (nx, ny), 2)

    def on_collide(self, other):
        pass
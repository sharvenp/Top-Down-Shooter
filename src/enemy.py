
from controllable import Controllable
from utils import Utils
from settings import Settings

import pygame as pg

class Enemy(Controllable):

    def __init__(self, position, players):
        Controllable.__init__(self)
        self.position = position
        self.players = players
        self.look_angle = 0

    def move(self):
        self.position = Utils.direction_position(self.position, self.look_angle, Settings.ENEMY_MOVEMENT_SPEED * Settings.DELTA_TIME)

    def turn(self):

        d = float('inf')
        closest_player = None
        for player in self.players:
            dist = Utils.get_distance(self.position, player.position)
            if dist < d:
                d = dist
                closest_player = player

        angle = Utils.get_look_angle(self.position, closest_player.position)
        self.look_angle = angle % 360

    def render(self, screen):
        pg.draw.circle(screen, Settings.ENEMY_COLOR, self.position, Settings.ENEMY_SIZE)

        nx, ny = Utils.direction_position(self.position, self.look_angle, 8)
        pg.draw.line(screen, (255, 0, 0), self.position, (nx, ny), 2)
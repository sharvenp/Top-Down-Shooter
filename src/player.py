
from controllable import Controllable
from bullet import Bullet
from collideable import Collideable
from health import Health
from utils import Utils
from settings import Settings

import pygame as pg
import math

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

    def cast_ray(self, pos, angle, enemies, ray_range):
    
        # Append all blocks that are not on a wall
        x, y = pos
        dx = math.cos(math.radians(angle)) * ray_range
        dy = math.sin(math.radians(angle)) * ray_range

        blocks = Utils.get_raycast_blocks(x, y, round(x + dx), round(y + dy))

        new_blocks = []
        hit_type = 0

        if blocks[0] != (x, y):
            blocks = blocks[::-1]

        for block in blocks:

            c, r = block

            if not ((0 <= c < Settings.WIDTH) and (0 <= r < Settings.HEIGHT)):
                hit_type = 1
                break
            
            if Utils.get_distance((x, y), (c, r)) > ray_range:
                break
            
            enemy_hit = None
            for enemy in enemies:
                if Utils.get_distance((c, r), enemy.position) <= Settings.ENEMY_SIZE:
                    enemy_hit = enemy
                    break
            
            if enemy_hit:
                hit_type = enemy_hit 
                break

            new_blocks.append(block)
            
        return new_blocks, hit_type

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
        old = self.rotation
        self.rotation = angle

        if Settings.DEBUG and self.rotation != old:
            print(f"New Player Angle: {self.rotation}")

    def shoot(self, enemies):

        if Settings.DEBUG:
            print("Player Shooting")

        blocks, hit = self.cast_ray(self.position, self.rotation, enemies, Settings.PLAYER_SHOOT_RANGE)
        
        if type(hit) != int: # Hit enemy object
            hit.deal_damage(Settings.PLAYER_DAMAGE)

        self.ray_data = [(blocks, hit)]

        # Old Projectile
        # nx, ny = Utils.direction_position(self.position, self.rotation, Settings.SHOOT_START_DIST)
        # bullet = Bullet((nx, ny), self.rotation, Settings.BULLET_SPEED, Settings.BULLET_COLOR_PLAYER)
        # return bullet

    def render(self, screen):
        pg.draw.circle(screen, Settings.PLAYER_COLOR, self.position, Settings.PLAYER_SIZE)

        nx, ny = Utils.direction_position(self.position, self.rotation, Settings.SHOOT_START_DIST)
        pg.draw.line(screen, Settings.PLAYER_COLOR, self.position, (nx, ny), 3)

        if self.ray_data:

            if Settings.AGENT_DEBUG or len(self.ray_data) == 1:
                for ray in self.ray_data:
                    blocks, hit_type = ray
                    if blocks:
                        color = (100, 0, 100)
                        if hit_type == 1:
                            color = (100, 100, 100)
                        elif type(hit_type) != int:
                            color = (0, 100, 0)
                        
                        thickness = 1

                        if len(self.ray_data) == 1:
                            thickness = 4

                        pg.draw.line(screen, color, self.position, blocks[-1], thickness) 
                    
            self.ray_data = []

        if Settings.AGENT_PLAYER and Settings.AGENT_DEBUG:
            pg.draw.circle(screen, (0, 255, 0), self.position, Settings.AWARENESS_RANGE, 1)

    def on_collide(self, other):
        pass
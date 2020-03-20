
from enemy import Enemy
from enemy_controller import EnemyController
from settings import Settings
from utils import Utils

import random
import math  

class Spawner:

    def __init__(self, env):
        self.env = env
        self.ticks = 0
        
        self.curr_bound = Settings.SPAWN_BOUND_START

    def spawn(self):

        if self.ticks % Settings.SPAWN_INTERVAL == 0:

            spawn_count = math.ceil(random.random() * self.curr_bound)

            for s in range(spawn_count):
                pos = Utils.on_circle_point((Settings.WIDTH//2, Settings.HEIGHT//2), 360)
                enemy = Enemy(pos, self.env[0])
                enemy.attach_controller(EnemyController(enemy))
                self.env[2].append(enemy)

            if Settings.DEBUG:
                print(f"Spawned {spawn_count} enemies.")

        if self.ticks % Settings.GROWTH_INTERVAL == 0:

            self.curr_bound *= Settings.GROWTH_FACTOR

            self.curr_bound = min(self.curr_bound, Settings.SPAWN_UPPER_BOUND) # Clamp it

            if Settings.DEBUG:
                print(f"Update Spawn Bound: {self.curr_bound}")
        
        self.ticks += 1
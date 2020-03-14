
from spawner import Spawner
from player import Player
from enemy import Enemy
from human_controller import HumanController
from enemy_controller import EnemyController
from settings import Settings

import pygame as pg
import time as t

class View:

    def __init__(self):

        self.screen = pg.display.set_mode((Settings.WIDTH, Settings.HEIGHT))    
        pg.display.set_caption("Top Down Shooter")

        player = Player((Settings.WIDTH//2, Settings.HEIGHT//2))
        player_controller = player.attach_controller(HumanController(player, {"FORWARD":pg.K_w, "BACKWARD":pg.K_s}))

        players = [player]
        
        enemy = Enemy((50, 50), players)
        enemy.attach_controller(EnemyController(enemy))
        
        # 0: Players, 1: Player Projectiles, 2: Enemies, 3: Enemy Projectiles
        self.env = {0:players, 1:[], 2:[enemy], 3:[]}

        self.spawner = Spawner(self.env)

    def _render_all(self):

        self.screen.fill((0,0,0))

        all_objs = []
        for key in self.env:
            all_objs += self.env[key]

        for obj in all_objs:
            obj.render(self.screen)

    def _delete_element(self, delete_lst):

        for ele_tup in delete_lst:
            element, key = ele_tup
            lst = self.env[key]
            popped = lst.pop(lst.index(element))
            if Settings.DEBUG:
                print(f"Deleted: {type(popped)}")
                print(delete_lst)
            del popped

    def run(self):

        while True:
 
            e = pg.event.poll()

            if (e.type == pg.QUIT):
                quit(0)

            deleted_elements = []

            for key in self.env:
                for obj in self.env[key]:
                    if obj.destroyed:
                        deleted_elements.append((obj, key))
                        continue
                    
                    if key % 2 == 0: # Controllable
                        obj.controller.handle(e, self.env)
                    else: # Projectile
                        obj.step()

            self._delete_element(deleted_elements)

            self.spawner.spawn()

            self._render_all()
            pg.display.update()
            t.sleep(Settings.DELTA_TIME)



from spawner import Spawner
from player import Player
from enemy import Enemy
from score_manager import ScoreManager
from human_controller import HumanController
from enemy_controller import EnemyController
from settings import Settings

import pygame as pg
import time as t

class View:

    def __init__(self):

        self.screen = pg.display.set_mode((Settings.WIDTH, Settings.HEIGHT))    
        pg.display.set_caption("Top Down Shooter")

    def _render_all(self):

        self.screen.fill(Settings.BACKGROUND_COLOR)

        for key in self.env:
            for obj in self.env[key]:
                obj.render(self.screen)

    def _delete_elements(self, delete_lst):

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

            player = Player((Settings.WIDTH//2, Settings.HEIGHT//2))
            player_controller = player.attach_controller(HumanController(player, {"FORWARD":pg.K_w, "BACKWARD":pg.K_s}))

            # 0: Players, 1: Player Projectiles, 2: Enemies, 3: Enemy Projectiles
            self.env = {0:[player], 1:[], 2:[], 3:[]}

            self.spawner = Spawner(self.env)

            ScoreManager.SCORE = 0

            while True:
    
                e = pg.event.poll()

                if (e.type == pg.QUIT):
                    quit(0)
                
                if len(self.env[0]) == 0:
                    break 

                deleted_elements = []
                collidable_elements = []
        
                # Check Collisions
                for key in self.env:
                    collidable_elements += self.env[key]
                for i in range(len(collidable_elements)):
                    for j in range(i+1, len(collidable_elements)):
                        result = collidable_elements[i].check_collide(collidable_elements[j])
                        if (result):
                            collidable_elements[i].on_collide(collidable_elements[j])
                            collidable_elements[j].on_collide(collidable_elements[i])

                # Handle all GameObjects
                for key in self.env:
                    for obj in self.env[key]:
                        if obj.destroyed:
                            deleted_elements.append((obj, key))
                            continue
                        
                        if key % 2 == 0: # Controllable
                            obj.controller.handle(e, self.env)
                        else: # Projectile
                            obj.step()

                self._delete_elements(deleted_elements)

                self.spawner.spawn()

                self._render_all()
                pg.display.update()
                t.sleep(Settings.DELTA_TIME)

            print(f"Game Over. Score: {ScoreManager.SCORE}")


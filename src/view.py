
from spawner import Spawner
from player import Player
from enemy import Enemy
from score_manager import ScoreManager
from human_controller import HumanController
from enemy_controller import EnemyController
from agent_controller import AgentController
from settings import Settings

import pygame as pg
import time as t
from PIL import Image

class View:

    def __init__(self):

        self.screen = pg.display.set_mode((Settings.WIDTH, Settings.HEIGHT))    
        pg.display.set_caption("Top Down Shooter")

    def _render_all(self):

        self.screen.fill(Settings.FLOOR_COLOR)

        for key in self.env:
            for obj in self.env[key]:
                obj.render(self.screen)

        pg.display.update()

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

        player = Player((Settings.WIDTH//2, Settings.HEIGHT//2))
        if Settings.AGENT_PLAYER:
            player.attach_controller(AgentController(player)) 
        else:
            player.attach_controller(HumanController(player, {"FORWARD":pg.K_w, "BACKWARD":pg.K_s}))
        
        episode = 0
        start_time = t.time()

        while True:

            player.reset((Settings.WIDTH//2, Settings.HEIGHT//2))

            if Settings.AGENT_PLAYER:
                player.controller.reset_training_data()
                                        
            # 0: Players, 1: Player Projectiles, 2: Enemies, 3: Enemy Projectiles
            self.env = {0:[player], 1:[], 2:[], 3:[]}
            self.spawner = Spawner(self.env)

            ScoreManager.SCORE = 0

            while True:

                e = pg.event.poll()

                if (e.type == pg.QUIT):
                    quit(0)
                
                deleted_elements = []
                collidable_elements = []
                ScoreManager.TRIGGER = 0
        
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

                if player.destroyed: # Player dead
                    player.controller.add_reward(Settings.DIE_REWARD)                    
                    break
                else:
                    reward = Settings.ALIVE_REWARD
                    if ScoreManager.TRIGGER:
                        reward += Settings.KILL_REWARD
                    player.controller.add_reward(reward)


                self.spawner.spawn()

                self._render_all()
                # t.sleep(1/Settings.FRAME_RATE)

            if Settings.AGENT_PLAYER:
                episode += 1
                player.controller.train_wrapper(episode)
                elapsed_time = t.time() - start_time    
                time_str = t.strftime("%H:%M:%S", t.gmtime(elapsed_time)) 
                output_string = "Episode: {:0>5} Score: {:0>3} Reward: {:0>6} T+: {}".format(episode, ScoreManager.SCORE, sum(player.controller.rewards), time_str)
                print(output_string)
            else:
                print(f"Game Over. Score: {ScoreManager.SCORE}")


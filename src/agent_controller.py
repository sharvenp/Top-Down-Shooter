
from settings import Settings
from utils import Utils
from controller import Controller
from agent import Agent

import math
import numpy as np

"""
Agent Input:

- 20 normalized vision casts
- 20 object hit types for each raycast
- 1 awareness value (number of enemies in awareness radius / total enemies)

Agent Output:

- turn left
- turn right
- move forward
- move backward
- shoot

"""
class AgentController(Controller):

    def __init__(self, controlled_object):
        Controller.__init__(self, controlled_object)
        self.agent = Agent(Settings.ARCHITECTURE, Settings.LR, Settings.GAMMA, Settings.SAVE_INTERVAL, 
                           Settings.LOAD_MOST_RECENT_MODEL, Settings.SAVE_DIRECTORY)

    def reset_training_data(self):        
        self.states = []
        self.actions = []
        self.rewards = []

    def add_reward(self, reward):
        self.rewards.append(reward)

    def train_wrapper(self, episode):
        self.agent.train_episode(self.states, self.actions, self.rewards, episode)

    def cast_ray(self, pos, angle, enemies):
    
        # Append all blocks that are not on a wall
        x, y = pos
        dx = math.cos(math.radians(angle)) * Settings.FOV_RANGE
        dy = math.sin(math.radians(angle)) * Settings.FOV_RANGE

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
            
            if Utils.get_distance((x, y), (c, r)) > Settings.FOV_RANGE:
                break
            
            enemy_hit_check = False
            for enemy in enemies:
                if Utils.get_distance((c, r), enemy.position) <= Settings.ENEMY_SIZE:
                    enemy_hit_check = True
                    break
            
            if enemy_hit_check:
                hit_type = 2
                break

            new_blocks.append(block)
            
        return new_blocks, hit_type

    def handle(self, event, env):
        
        x = []
        x1 = []
        x2 = []
        awareness_value = 0

        curr_angle = self.controlled_object.rotation - (Settings.FOV // 2)
        curr_angle %= 360
        delta = Settings.FOV // Settings.NUM_RAYS
        ray_data = []

        for ray in range(Settings.NUM_RAYS):
            blocks, hit_type = self.cast_ray(self.controlled_object.position, curr_angle, env[2])
            ray_data.append((blocks, hit_type))
            curr_angle += delta
            curr_angle %= 360

            if blocks:
                x1.append(Utils.get_distance(blocks[-1], self.controlled_object.position) / Settings.FOV_RANGE)
            else:
                x1.append(0)
            x2.append(hit_type/2)


        self.controlled_object.ray_data = ray_data

        count = 0
        total = len(env[2])
        for enemy in env[2]:
            if Utils.get_distance(self.controlled_object.position, enemy.position) <= Settings.AWARENESS_RANGE:
                count += 1
        
        if total > 0:
            awareness_value = count / total

        x = x1 + x2 + [awareness_value]

        action = self.agent.get_state_action(x)

        if action == 0:
            self.controlled_object.turn((self.controlled_object.rotation + Settings.PLAYER_TURN_SPEED) % 360)
        elif action == 1:
            self.controlled_object.turn((self.controlled_object.rotation - Settings.PLAYER_TURN_SPEED) % 360)
        elif action == 2:
            self.controlled_object.move(1)
        elif action == 3:
            self.controlled_object.move(-1)
        elif action == 4:
            bullet = self.controlled_object.shoot()
            if bullet:
                env[1].append(bullet)

        self.states.append(np.asarray(x))
        self.actions.append(action)

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


        if not Settings.LOAD_MOST_RECENT_MODEL:
            self.agent._load_model(f"../models/chkpnt-{Settings.LO}.h5")

    def reset_training_data(self):        
        self.states = []
        self.actions = []
        self.rewards = []

    def add_reward(self, reward):
        self.rewards.append(reward)

    def train_wrapper(self, episode):
        self.agent.train_episode(self.states, self.actions, self.rewards, episode)

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
            blocks, hit_type = self.controlled_object.cast_ray(self.controlled_object.position, curr_angle, env[2], Settings.FOV_RANGE)
            ray_data.append((blocks, hit_type))
            curr_angle += delta
            curr_angle %= 360

            if blocks:
                x1.append(Utils.get_distance(blocks[-1], self.controlled_object.position) / Settings.FOV_RANGE)
            else:
                x1.append(0)

            if type(hit_type) == int:
                x2.append(hit_type/2)
            else:
                x2.append(1)


        self.controlled_object.ray_data = ray_data

        count = 0
        total = len(env[2])
        for enemy in env[2]:
            if Utils.get_distance(self.controlled_object.position, enemy.position) <= Settings.AWARENESS_RANGE:
                count += 1
        
        if total > 0:
            awareness_value = count / total

        x = x1 + x2 + [awareness_value] + [self.controlled_object.health / Settings.PLAYER_HEALTH]

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
            # bullet = self.controlled_object.shoot()
            # if bullet:
            #     env[1].append(bullet)
            self.controlled_object.shoot(env[2])


        self.states.append(np.asarray(x))
        self.actions.append(action)
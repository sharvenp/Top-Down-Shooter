
from controller import Controller

import pygame as pg

class EnemyController(Controller):

    def __init__(self, controlled_object):
        Controller.__init__(self, controlled_object)

    def handle(self, event, env):
        
        self.controlled_object.turn()
        self.controlled_object.move()        
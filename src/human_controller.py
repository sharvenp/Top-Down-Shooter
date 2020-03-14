
from controller import Controller
from settings import Settings

import pygame as pg

class HumanController(Controller):

    def __init__(self, controlled_object, control_scheme):
        Controller.__init__(self, controlled_object)
        self.control_scheme = control_scheme

    def handle(self, event, env):
        
        keys = pg.key.get_pressed()

        sign = 0

        if keys[self.control_scheme["FORWARD"]]:
            sign = 1
        if keys[self.control_scheme["BACKWARD"]]:
            sign = -1
            
        self.controlled_object.turn()

        if event.type == pg.MOUSEBUTTONDOWN:
            bullet = self.controlled_object.shoot()
            if bullet:
                env[1].append(bullet)

        if sign:
            angle = self.controlled_object.look_angle
            self.controlled_object.move(sign)        
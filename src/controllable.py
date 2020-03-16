
from game_object import GameObject

class Controllable(GameObject):

    def __init__(self, tag, position, rotation):
        GameObject.__init__(self, tag, position, rotation)

    def attach_controller(self, controller):
        self.controller = controller
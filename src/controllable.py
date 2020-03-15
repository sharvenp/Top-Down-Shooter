
from game_object import GameObject

class Controllable(GameObject):

    def __init__(self):
        GameObject.__init__(self)

    def attach_controller(self, controller):
        self.controller = controller
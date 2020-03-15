
from game_object import GameObject

class Projectile(GameObject):

    def __init__(self):
        GameObject.__init__(self)

    def step(self):
        raise NotImplementedError
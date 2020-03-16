
from game_object import GameObject

class Projectile(GameObject):

    def __init__(self, tag, position, rotation):
        GameObject.__init__(self, tag, position, rotation)

    def step(self):
        raise NotImplementedError
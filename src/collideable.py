
from utils import Utils

class Collideable:

    def __init__(self, radius):
        self.radius = radius

    def check_collide(self, other):
        dist = Utils.get_distance(self.position, other.position)
        return (dist - self.radius) <= other.radius

    def on_collide(self, other):
        raise NotImplementedError

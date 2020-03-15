
class GameObject:

    def __init__(self):
        self.destroyed = False

    def render(self, screen):
        raise NotImplementedError
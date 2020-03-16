
class GameObject:

    def __init__(self, tag, position, rotation):
        self.destroyed = False
        self.tag = tag
        self.position = position
        self.rotation = rotation

    def render(self, screen):
        raise NotImplementedError
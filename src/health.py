
from settings import Settings

class Health:

    def __init__(self, health):
        self.health = health

    def deal_damage(self, damage):
        
        if Settings.DEBUG:
            print(f"Tag: {self.tag} took {damage} damage. New HP: {self.health}")

        self.health -= damage

        if self.health <= 0:
            self.health = 0
            self.destroyed = True
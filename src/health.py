
from settings import Settings
from score_manager import ScoreManager

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

            if self.tag == 2: # Enemy
                for player in self.players:
                    ScoreManager.SCORE += Settings.KILL_SCORE
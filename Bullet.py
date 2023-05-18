from GameObject import GameObject
from utils import load_sprite


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite('bullet', '0'), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity

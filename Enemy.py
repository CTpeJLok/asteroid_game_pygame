import random
from pygame.transform import rotozoom

from GameObject import GameObject
from settings import *
from utils import load_sprite, get_random_velocity


class Enemy(GameObject):
    def __init__(self, position, create_asteroid_callback):
        self.create_asteroid_callback = create_asteroid_callback

        scale = random.randint(ENEMY.SIZE_MIN, ENEMY.SIZE_MAX) / 100
        sprite = rotozoom(load_sprite('enemy', '0'), 0, scale)

        super().__init__(position, sprite, get_random_velocity(ENEMY.SPEED_MIN, ENEMY.SPEED_MAX))

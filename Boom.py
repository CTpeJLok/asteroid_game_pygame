from pygame import Vector2

from utils import load_sprite
from settings import *


class Boom:
    def __init__(self, position):
        self.position = Vector2(position)
        self.sprite = load_sprite('boom', '0')
        self.radius = self.sprite.get_width() / 2
        self.state = 0

    def draw(self, surface):
        self.sprite = load_sprite('boom', f'{int(self.state)}')
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)
        self.state += BOOM.COUNT / (SCREEN.FPS * BOOM.SPEED)

    def is_end(self):
        return self.state >= BOOM.COUNT

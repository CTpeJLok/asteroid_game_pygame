from pygame import Vector2
from pygame.transform import rotozoom

from utils import load_sprite


class Welcome:
    def __init__(self, position, sprite_name='0'):
        self.position = Vector2(position)
        self.sprite = rotozoom(load_sprite('welcome', sprite_name), 0, 2)
        self.radius = self.sprite.get_width() / 2

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        blit_position.y += 100
        surface.blit(self.sprite, blit_position)

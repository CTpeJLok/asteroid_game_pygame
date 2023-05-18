from pygame.math import Vector2
from pygame.transform import rotozoom

from GameObject import GameObject
from Bullet import Bullet
from settings import *
from utils import load_sprite

UP = Vector2(0, -1)


class Player(GameObject):
    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)
        self.isAcceleration = False

        super().__init__(position, load_sprite('player', '0'), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = PLAYER.SPEED_ROTATE * sign
        self.direction.rotate_ip(angle)
        self.sprite = load_sprite('player', '0_right' if sign == 1 else '0_left')

    def front(self):
        self.sprite = load_sprite('player', '0_front')

        if self.isAcceleration:
            self.velocity += self.direction * (PLAYER.SPEED_MOVE + PLAYER.SPEED_ACCELERATION)
        else:
            self.velocity += self.direction * PLAYER.SPEED_MOVE

    def back(self):
        self.sprite = load_sprite('player', '0_back')

        if self.isAcceleration:
            self.velocity -= self.direction * (PLAYER.SPEED_MOVE + PLAYER.SPEED_ACCELERATION)
        else:
            self.velocity -= self.direction * PLAYER.SPEED_MOVE

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        self.velocity -= self.velocity
        self.sprite = load_sprite('player', '0')

    def shoot(self):
        bullet_velocity = self.direction * BULLET.SPEED_ACCELERATION + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)

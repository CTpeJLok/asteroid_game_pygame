import random

from pygame import Color
from pygame.image import load
from pygame.math import Vector2


def load_sprite(group, name, with_alpha=True):
    path = f'images/{group}/{name}.png'
    loaded_sprite = load(path)

    return loaded_sprite.convert_alpha() if with_alpha else loaded_sprite.convert()


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def print_text(surface, x, y, auchor, text, font, color=Color("tomato")):
    text_surface = font.render(text, False, color)
    w, h = font.size(text)

    if auchor == 'ld':
        h = -h
    elif auchor == 'l':
        pass
    else:
        w = -w

    # if auchor != 'l':
    #     w = -w
    # elif auchor != 'ld':
    #     w = -w
    #     # h = -h

    rect = text_surface.get_rect()
    position = Vector2(surface.get_size()) / 2
    position.x += x + w / 2
    position.y += y + h / 2
    rect.center = position

    surface.blit(text_surface, rect)

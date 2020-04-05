import game.map_entity
import game.resources
from game.resources import map_images
import pyglet


class LargeTree(game.map_entity.MapEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def create(self, **kwargs):
        y = self.get_y(kwargs['vpos'])
        x = self.get_x(kwargs['hpos'])
        self.content += [self.get_sprite(map_images[65], x, y+64)]
        self.content += [self.get_sprite(map_images[66], x + 32, y + 64)]
        self.content += [self.get_sprite(map_images[67], x+64, y + 64)]
        self.content += [self.get_sprite(map_images[53], x, y + 32)]
        self.content += [self.get_sprite(map_images[54], x + 32, y + 32)]
        self.content += [self.get_sprite(map_images[55], x + 64, y + 32)]
        self.content += [self.get_sprite(map_images[41], x, y)]
        self.content += [self.get_sprite(map_images[42], x + 32, y)]
        self.content += [self.get_sprite(map_images[43], x + 64, y)]




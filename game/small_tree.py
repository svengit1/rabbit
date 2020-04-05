import game.map_entity
import game.resources
from game.resources import map_images
import pyglet


class SmallTree(game.map_entity.MapEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def create(self, **kwargs):
        y = self.get_y(kwargs['vpos'])
        x = self.get_x(kwargs['hpos'])
        self.content += [self.get_sprite(map_images[51], x, y+32)]
        self.content += [self.get_sprite(map_images[52], x+32, y+32)]
        self.content += [self.get_sprite(map_images[39], x, y)]
        self.content += [self.get_sprite(map_images[40], x+32, y)]




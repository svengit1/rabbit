import game.map_entity
import game.resources
from game.resources import map_images
import pyglet


class Cloud(game.map_entity.MapEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def create(self, **kwargs):
        y = self.get_y(kwargs['vpos'])
        x = self.get_x(kwargs['hpos'])

        self.content += [self.get_sprite(map_images[1], x, y)]
        self.content += [self.get_sprite(map_images[2], x+32, y)]
        self.content += [self.get_sprite(map_images[3], x+64, y)]
        self.content += [self.get_sprite(map_images[4], x+96, y)]
        self.content += [self.get_sprite(map_images[5], x+128, y)]
        self.content += [self.get_sprite(map_images[13], x, y+32)]
        self.content += [self.get_sprite(map_images[14], x+32, y+32)]
        self.content += [self.get_sprite(map_images[15], x+64, y+32)]
        self.content += [self.get_sprite(map_images[16], x+96, y+32)]

import pyglet
import game.map_entity
import game.resources
from game.resources import map_images


class Platform(game.map_entity.MapEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.middle = map_images[225]

    def create(self, **kwargs):
        assert kwargs['size'] >= 4, "Size has to be greater or equal two"
        y = self.get_y(kwargs['vpos'])
        x = self.get_x(kwargs['hpos'])
        self.content = [self.get_sprite(map_images[i[0]], i[1], y)
                        for i in [(217, x), (218, x + 32)]]

        self.content += [self.get_sprite(self.middle, x + 32*2 + i*32, y)
                         for i in range(0, kwargs['size'] - 4)]

        self.content += [self.get_sprite(map_images[i[0]], i[1], y)
                         for i in [(223, x + (kwargs['size']-2)*32), (224, x + (kwargs['size']-2)*32 + 32)]]


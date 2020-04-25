import pyglet
import game.map_entity
import game.resources
from game.resources import map_images
import pymunk


class MovingPlatform(game.map_entity.MapEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.middle = map_images[225]
        self.space = kwargs['space']

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
        static_line = pymunk.Segment(self.space.static_body, (x+32 , y+32), (x + 32 + (kwargs['size']-2)*32, y+32), 0.0)
        static_line.friction = 1.0
        self.space.add(static_line)


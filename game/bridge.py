import game.map_entity
import game.resources
from game.resources import map_images
import pyglet
import pymunk


class Bridge(game.map_entity.MapEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.middle = []
        self.left = []
        self.right = []
        self.space = kwargs['space']
        self.lines = []

    def create(self, **kwargs):
        assert kwargs['size'] >= 8, "Size has to be greater or equal eight"
        y = self.get_y(kwargs['vpos'])
        x = self.get_x(kwargs['hpos'])
        span = kwargs['size'] * 32
        rx = x + span - 32 * 3
        mx = x + 3 * 32

        self.left = [self.get_sprite(map_images[i[0]], i[1], i[2])
                     for i in [(121, x, y), (109, x, y - 32), (97, x, y - 64),
                               (122, x + 32, y), (110, x + 32, y - 32), (98, x + 32, y - 64),
                               (123, x + 64, y), (111, x + 64, y - 32), (99, x + 64, y - 64)]]
        for i in range(0, kwargs['size'] - 6):
            self.middle += [self.get_sprite(map_images[i[0]], i[1], i[2])
                                    for i in [(124, mx + i * 32, y),
                                              (112, mx + i * 32, y - 32),
                                              (100, mx + i * 32, y - 64)]]

        self.right = [self.get_sprite(map_images[i[0]], i[1], i[2])
                        for i in [(126, rx, y), (114, rx, y - 32), (102, rx, y - 64),
                                  (127, rx + 32, y), (115, rx + 32, y - 32), (103, rx + 32, y - 64),
                                  (128, rx + 64, y), (116, rx + 64, y - 32), (104, rx + 64, y - 64)]]


        static_line1 = pymunk.Segment(self.space.static_body, (x + 32, y),
                                     (x + 96, y-48), 0.0)

        static_line2 = pymunk.Segment(self.space.static_body, (x + 96, y-48),
                                     (x + 96 +((kwargs['size']-6)*32), y-48), 0.0)

        static_line3 = pymunk.Segment(self.space.static_body, (x + 96 +((kwargs['size']-6)*32), y-48),
                                     (x + 96 +((kwargs['size']-4)*32), y), 0.0)

        static_line3.friction = 1
        static_line2.friction = 1
        static_line1.friction = 1
        self.lines =[static_line2, static_line1, static_line3]
        self.space.add(static_line3)
        self.space.add(static_line2)
        self.space.add(static_line1)





import game.map_entity
import game.resources
from game.resources import map_images
import pyglet


class Bridge(game.map_entity.MapEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        self.middle = []
        for i in range(0, kwargs['size'] - 6):
            self.middle += [self.get_sprite(map_images[i[0]], i[1], i[2])
                                    for i in [(124, mx + i * 32, y),
                                              (112, mx + i * 32, y - 32),
                                              (100, mx + i * 32, y - 64)]]

        self.right = [self.get_sprite(map_images[i[0]], i[1], i[2])
                        for i in [(126, rx, y), (114, rx, y - 32), (102, rx, y - 64),
                                  (127, rx + 32, y), (115, rx + 32, y - 32), (103, rx + 32, y - 64),
                                  (128, rx + 64, y), (116, rx + 64, y - 32), (104, rx + 64, y - 64)]]




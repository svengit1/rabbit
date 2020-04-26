import game.map_entity
import game.resources
from game.resources import map_images, segment_height, segment_width
import pyglet
import pymunk
from game.map_entity import MapEntity


class Bridge(MapEntity):
    def __init__(self, **kwargs):
        self.space = kwargs['space']
        self.y = kwargs['vpos']*segment_height
        self.x = kwargs['hpos']*segment_width
        bridge_width = kwargs['width']
        self.image = Bridge.create_image(bridge_width)
        slope_left = pymunk.Segment(self.space.static_body, (self.x + 32, self.y),
                                    (self.x + 96, self.y-48), 0.0)
        flat = pymunk.Segment(self.space.static_body, (self.x + 96, self.y-48),
                              (self.x + 96 + (bridge_width-6)*32, self.y-48), 0.0)
        slope_right = pymunk.Segment(self.space.static_body, (self.x + 96 + (bridge_width-6)*32, self.y-48),
                                     (self.x + 96 + (bridge_width-4)*32, self.y), 0.0)
        slope_left.friction, flat.friction, slope_right.friction = 1, 1, 1
        self.lines = []
        self.lines = [slope_left, flat, slope_right]
        self.space.add(self.lines)

    @staticmethod
    def create_image(width):
        assert width >= 8, "Width has to be greater or equal eight"
        height = 3
        image = pyglet.image.Texture.create(width*32, height*32)
        for bridge_left_part in [(121, 0, 64), (109, 0, 32), (97, 0, 0),
                                 (122, 32, 64), (110, 32, 32), (98, 32, 0),
                                 (123, 64, 64), (111, 64, 32), (99, 64, 0)]:
            image = Bridge.add_image(image, bridge_left_part[0], bridge_left_part[1], bridge_left_part[2])

        offset = 3 * segment_width
        for bridge_flat_part in range(0, width - 6):
            for flat_part_seg in [(124, offset + bridge_flat_part * 32, 64),
                                  (112, offset + bridge_flat_part * 32, 32),
                                  (100, offset + bridge_flat_part * 32, 0)]:
                image = Bridge.add_image(image, flat_part_seg[0], flat_part_seg[1], flat_part_seg[2])
        offset += (width-6) * segment_width
        for bridge_right_part in [(126, offset, 64), (114, offset, 32), (102, offset, 0),
                                  (127, offset + 32, 64), (115, offset + 32, 32), (103, offset + 32, 0),
                                  (128, offset + 64, 64), (116, offset + 64, 32), (104, offset + 64, 0)]:
            image = Bridge.add_image(image, bridge_right_part[0], bridge_right_part[1], bridge_right_part[2])

        image.anchor_y = 64

        return image







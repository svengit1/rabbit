import pyglet
import pymunk
from pymunk.body import Body
import math


import resources
from map_objects.map_entity import MapEntity
from resources import map_images, segment_height, segment_width


class Bridge(MapEntity):
    def __init__(self, **kwargs):
        self.space = kwargs['space']
        self.y = kwargs['vpos'] * segment_height
        self.x = kwargs['hpos'] * segment_width
        self.width = kwargs['width']
        self.image = Bridge.create_image(self.width)
        self.__init_physics()

    def __init_physics(self):
        vs = [(-segment_height, -segment_width), (-segment_height, -(self.width - 1) * segment_width),
              (0, -(self.width - 1) * segment_width),
              (0, -segment_width)]
        self.body = pymunk.Body(mass=0, moment=0, body_type=Body.KINEMATIC)
        self.shape = pymunk.Poly(self.body, vs)
        self.shape.friction = 4.0
        self.shape.elasticity = 0
        self.shape.collision_type = 3
        self.body.angle = 0.5 * math.pi
        self.space.add(self.body, self.shape)
        self.body.position = self.x, self.y

    @staticmethod
    def create_image(width):
        assert width >= 3, "Width has to be greater or equal three"
        height = 2
        image = pyglet.image.Texture.create(width * 32, height * 32)
        image = Bridge.add_image(image, 121, 0, 32)
        offset = segment_width
        for bridge_flat_part in range(0, width - 2):
            for flat_part_seg in [(129, offset + bridge_flat_part * 32, 32),
                                  (117, offset + bridge_flat_part * 32, 0)]:
                image = Bridge.add_image(image, flat_part_seg[0],
                                         flat_part_seg[1], flat_part_seg[2])
        offset += (width - 2) * segment_width
        image = Bridge.add_image(image, 128, offset, 32)

        image.anchor_y = 32

        return image

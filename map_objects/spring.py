import math

import pyglet
import pymunk
from pymunk.body import Body

from map_objects.map_entity import MapEntity
from resources import segment_height, segment_width


class Spring(MapEntity):
    def __init__(self, **kwargs):
        self.space = kwargs['space']
        self.width = 32
        self.y = kwargs['vpos'] * segment_height
        self.x = kwargs['hpos'] * segment_width
        self.image = Spring.create_image(self.width)
        self.__init_physics()

    def __init_physics(self):
        vs = [(0, 0), (0, self.width),
              (self.width, segment_height),
              (segment_height, -segment_width)]
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
        assert width >= 4, "Width has to be greater or equal than four"
        image = pyglet.image.Texture.create(32, 96)
        image = Spring.add_image(image, 133, 0, 0)
        image = Spring.add_image(image, 145, 0, 32)
        image = Spring.add_image(image, 157, 0, 64)
        return image

        # image = Spring.add_image(image, 217, offset, 0)
        # offset += segment_width
        # image = Spring.add_image(image, 218, offset, 0)
        # offset += segment_width
        # for j in range(width - 4):
        #     image = Platform.add_image(image, 225, offset, 0)
        #     offset += segment_width
        # image = Platform.add_image(image, 223, offset, 0)
        # offset += segment_width
        # image = Platform.add_image(image, 224, offset, 0)
        # return image

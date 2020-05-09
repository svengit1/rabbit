import math

import pyglet
import pymunk
from pymunk.body import Body

from game.map_entity import MapEntity
from game.resources import segment_height, segment_width


class Platform(MapEntity):
    def __init__(self, **kwargs):
        self.space = kwargs['space']
        self.width = kwargs['width']
        self.y = kwargs['vpos'] * segment_height
        self.x = kwargs['hpos'] * segment_width
        self.image = Platform.create_image(self.width)
        self.__init_physics()

    def __init_physics(self):
        vs = [(0, -segment_width), (0, -(self.width - 1) * segment_width),
              (segment_height, -(self.width - 1) * segment_width),
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
        image = pyglet.image.Texture.create(width * 32, 32)
        offset = 0
        image = Platform.add_image(image, 217, offset, 0)
        offset += segment_width
        image = Platform.add_image(image, 218, offset, 0)
        offset += segment_width
        for j in range(width - 4):
            image = Platform.add_image(image, 225, offset, 0)
            offset += segment_width
        image = Platform.add_image(image, 223, offset, 0)
        offset += segment_width
        image = Platform.add_image(image, 224, offset, 0)
        return image

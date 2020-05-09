import math

import pyglet
import pymunk
from pymunk.body import Body

from game.platform import Platform
from game.resources import segment_height, segment_width


class MovingPlatform(pyglet.sprite.Sprite):
    def __init__(self, **kwargs):
        self.platform_width = kwargs['width']
        self.space = kwargs['space']
        self.velocity = kwargs['velocity']
        self.initial_position = tuple(
            [i * segment_width for i in kwargs['initial_position']])
        self.path_length = kwargs['path_length']
        kwargs.pop('space')
        kwargs.pop('width')
        kwargs.pop('velocity')
        kwargs.pop('initial_position')
        kwargs.pop('path_length')
        x, y = self.initial_position
        super().__init__(img=Platform.create_image(self.platform_width),
                         x=x,
                         y=y,
                         **kwargs)
        self.__init_physics()

    def __init_physics(self):
        vs = [(0, -segment_width),
              (0, -(self.platform_width - 1) * segment_width),
              (segment_height, -(self.platform_width - 1) * segment_width),
              (segment_height, -segment_width)]
        self.body = pymunk.Body(mass=0, moment=0, body_type=Body.KINEMATIC)
        self.shape = pymunk.Poly(self.body, vs)
        self.shape.friction = 4.0
        self.shape.collision_type = 3
        self.body.angle = 0.5 * math.pi
        self.space.add(self.body, self.shape)
        self.body.position = self.initial_position
        self.body.velocity = self.velocity

    def update(self, dt):
        self.x = self.body.position.x
        self.y = self.body.position.y
        p = math.sqrt((self.initial_position[0] - self.x)**2 +
                      (self.initial_position[1] - self.y)**2)
        if math.isclose(p, self.path_length,
                        abs_tol=0.9) and self.body.velocity == self.velocity:
            # reverse velocity
            self.body.velocity = tuple([i * -1 for i in self.body.velocity])
        if math.isclose(p, 0,
                        abs_tol=0.9) and self.body.velocity != self.velocity:
            # reverse velocity
            self.body.velocity = tuple([i * -1 for i in self.body.velocity])

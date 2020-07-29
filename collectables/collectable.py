import math

import pymunk
from pyglet.sprite import Sprite

from resources import segment_height, segment_width


class Collectable(Sprite):
    def __init__(self, image, mass, **kwargs):
        self.space = kwargs['space']
        x = kwargs['hpos'] * segment_width
        y = kwargs['vpos'] * segment_height
        kwargs.pop('hpos')
        kwargs.pop('vpos')
        kwargs.pop('space')
        super().__init__(img=image, x=x, y=y, **kwargs)
        self.__init_physics__(mass)

    def __init_physics__(self, mass=0):
        body_type = pymunk.Body.KINEMATIC
        if mass:
            body_type = pymunk.Body.DYNAMIC
        vs = [(0, 0), (0, -32), (32, -32), (32, 0)]
        moment = pymunk.moment_for_poly(mass, vs)
        self.body = pymunk.Body(mass=mass, moment=moment, body_type=body_type)
        self.shape = pymunk.Poly(self.body, vs)
        self.body.position = self.x, self.y
        self.body.angle = 0.5 * math.pi
        self.space.add(self.body, self.shape)

    def update(self, dt):
        self.x = self.body.position.x
        self.y = self.body.position.y

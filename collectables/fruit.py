import math

import pyglet
import pymunk

from resources import map_images, segment_height, segment_width


class Fruit(pyglet.sprite.Sprite):
    CARROT = 216
    GRAPE = 204
    LEMON = 192
    PEAR = 180

    def __init__(self, *args, **kwargs):
        self.space = kwargs['space']
        x = kwargs['hpos'] * segment_width
        y = kwargs['vpos'] * segment_height
        image = kwargs['type']
        self.points = kwargs['points']
        kwargs.pop('hpos')
        kwargs.pop('vpos')
        kwargs.pop('space')
        kwargs.pop('type')
        kwargs.pop('points')
        super().__init__(img=map_images[image], x=x, y=y, **kwargs)
        self.__init_physics()

    def __init_physics(self):
        vs = [(0, 0), (0, -32), (32, -32), (32, 0)]
        self.body = pymunk.Body(mass=0,
                                moment=0,
                                body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Poly(self.body, vs)
        self.body.position = self.x, self.y
        self.body.angle = 0.5 * math.pi
        self.space.add(self.body, self.shape)
        self.shape.collision_type = 2
        self.shape.sprite = self

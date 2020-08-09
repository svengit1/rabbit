import pyglet
from pyglet.sprite import Sprite
from resources import segment_height, segment_width
import pymunk
from map_objects.map_entity import MapEntity
import math


class Crate(Sprite):
    def __init__(self, **kwargs):
        self.space = kwargs['space']
        x = kwargs['hpos'] * segment_width
        y = kwargs['vpos'] * segment_height
        kwargs.pop('hpos')
        kwargs.pop('vpos')
        kwargs.pop('space')
        image = pyglet.resource.image('crate-s.png')
        image.anchor_x = 15
        image.anchor_y = 32
        super().__init__(img=image, **kwargs)
        self.x, self.y = x, y

        self.__init_physics__()

    def __init_physics__(self):
        mass = 10
        body_type = pymunk.Body.DYNAMIC
        vs = [(-15, 0), (-15, 32), (15, 32), (15, 0)]
        moment = pymunk.moment_for_poly(mass, vs)
        self.body = pymunk.Body(mass=mass, moment=moment, body_type=body_type)
        self.shape = pymunk.Poly(self.body, vs)
        self.body.position = self.x, self.y
        self.shape.friction = 0.6
        self.shape.elasticity = 0.5
        self.body.center_of_gravity = 0, 16
        self.shape.collision_type = 3
        self.space.add(self.body, self.shape)

    def update(self, dt):
        self.rotation = math.degrees(-self.body.angle) + 180
        self.x = self.body.position.x
        self.y = self.body.position.y

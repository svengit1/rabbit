
import pyglet
import pymunk
from pymunk.body import Body

import resources
from map_objects.map_entity import MapEntity


class Platform(MapEntity):
    PLATFORM_LEFT_END = pyglet.resource.image("tile-14s.png")
    PLATFORM_MIDDLE = pyglet.resource.image('tile-15s.png')
    PLATFORM_RIGHT_END = pyglet.resource.image('tile-16s.png')

    def __init__(self, **kwargs):
        self.space = kwargs['space']
        self.width = kwargs['width']
        self.hpos = kwargs['hpos']
        self.vpos = kwargs['vpos']
        self.y = kwargs['vpos'] * resources.segment_height
        self.x = kwargs['hpos'] * resources.segment_width
        self.image = Platform.create_image(self.width)
        self.__init_physics()
        self.image = Platform.create_image(self.width)

    def __init_physics(self):
        vs = [(resources.segment_width - 32, 0), (self.width * resources.segment_width, 0),
              (self.width * resources.segment_width, resources.segment_height),
              (resources.segment_width - 32, resources.segment_height)]
        self.body = pymunk.Body(mass=0, moment=0, body_type=Body.KINEMATIC)
        self.shape = pymunk.Poly(self.body, vs)
        self.shape.friction = 4.0
        self.shape.elasticity = 0
        self.shape.collision_type = 3
        self.body.player_on_the_platform = False
        self.space.add(self.body, self.shape)
        self.body.position = self.x, self.y

    @staticmethod
    def create_image(width):
        assert width >= 3, "Width has to be greater or equal than three"
        segment_width = 32
        container_image = pyglet.image.Texture.create(width * resources.segment_width, resources.segment_height)
        offset = 0
        container_image.blit_into(Platform.PLATFORM_LEFT_END.get_image_data(), offset, 0, 0)
        offset += resources.segment_width
        for i in range(width - 2):
            container_image.blit_into(Platform.PLATFORM_MIDDLE.get_image_data(), offset, 0, 0)
            offset += segment_width
        container_image.blit_into(Platform.PLATFORM_RIGHT_END.get_image_data(), offset, 0, 0)
        return container_image

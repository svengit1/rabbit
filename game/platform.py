import pyglet
from game.resources import map_images, segment_width, segment_height
import pymunk
from game.map_entity import MapEntity


class Platform(MapEntity):
    def __init__(self, **kwargs):
        self.space = kwargs['space']
        self.width = kwargs['width']
        self.y = kwargs['vpos'] * segment_height
        self.x = kwargs['hpos'] * segment_width
        self.image = Platform.create_image(self.width)
        static_line = pymunk.Segment(self.space.static_body, (self.x + segment_width, self.y+segment_height),
                                     (self.x + segment_width + (self.width-2) * segment_width,
                                      self.y + segment_height), 0.0)
        static_line.friction = 1.0
        self.space.add(static_line)

    @staticmethod
    def create_image(width):
        assert width >= 4, "Width has to be greater or equal than four"
        image = pyglet.image.Texture.create(width*32, 32)
        offset = 0
        image = Platform.add_image(image, 217, offset, 0)
        offset += segment_width
        image = Platform.add_image(image, 218, offset, 0)
        offset += segment_width
        for j in range(width-4):
            image = Platform.add_image(image, 225, offset, 0)
            offset += segment_width
        image = Platform.add_image(image, 223, offset, 0)
        offset += segment_width
        image = Platform.add_image(image, 224, offset, 0)
        return image

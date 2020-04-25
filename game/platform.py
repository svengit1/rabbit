import pyglet
import game.resources
from game.resources import map_images, segment_width, segment_height
import pymunk
import pyglet.gl as gl

class Platform:
    def __init__(self, **kwargs):
        self.space = kwargs['space']
        self.width = kwargs['width']
        self.y = kwargs['vpos'] * self.segment_height
        self.x = kwargs['hpos'] * self.segment_width
        self.image = Platform.create_image(self.width)
        static_line = pymunk.Segment(self.space.static_body, (self.x + segment_width, self.y+segment_height),
                                     (self.x + segment_width + (self.width-2) * segment_width,
                                      self.y + segment_height), 0.0)
        static_line.friction = 1.0
        self.space.add(static_line)

    @staticmethod
    def add_image(image, image_id, position_offset):
        image.blit_into(map_images[image_id].get_image_data(), position_offset, 0, 0)
        new_offset = position_offset + segment_width
        return image, new_offset

    @staticmethod
    def create_image(width):
        assert width >= 4, "Width has to be greater or equal than four"
        image = pyglet.image.Texture.create(width*32, 32)
        offset = 0
        image, offset = Platform.add_image(image, 217, offset)
        image, offset = Platform.add_image(image, 218, offset)
        for j in range(width-4):
            image, offset = Platform.add_image(image, 225, offset)
        image, offset = Platform.add_image(image, 223, offset)
        image, offset = Platform.add_image(image, 224, offset)
        return image

    def draw(self):
        gl.glEnable(gl.GL_BLEND)
        self.image.blit(self.x, self.y)
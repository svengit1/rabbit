import pyglet
import game.resources
from game.resources import map_images
import pymunk
import pyglet.gl as gl

class Platform:
    def __init__(self, **kwargs):
        self.space = kwargs['space']
        self.width = kwargs['width']
        self.segment_width = 32
        self.segment_height = 32
        self.y = kwargs['vpos'] * self.segment_height
        self.x = kwargs['hpos'] * self.segment_width
        self.image = self.create_image(self.width)
        static_line = pymunk.Segment(self.space.static_body, (self.x+self.segment_width , self.y+self.segment_height),
                                     (self.x + self.segment_width + (self.width-2) * self.segment_width,
                                      self.y + self.segment_height), 0.0)
        static_line.friction = 1.0
        self.space.add(static_line)

    def add_image(self, image, id, offset):
        image.blit_into(map_images[id].get_image_data(), offset, 0, 0)
        new_offset = offset + self.segment_width
        return image, new_offset
        
    def create_image(self, width):
        assert width >= 4, "Width has to be greater or equal than four"
        image = pyglet.image.Texture.create(width*32, 32)
        offset = 0
        image, offset = self.add_image(image, 217, offset)
        image, offset = self.add_image(image, 218, offset)
        for j in range(width-4):
            image, offset = self.add_image(image, 225, offset)
        image, offset = self.add_image(image, 223, offset)
        image, offset = self.add_image(image, 224, offset)
        return image

    def draw(self):
        gl.glEnable(gl.GL_BLEND)
        self.image.blit(self.x, self.y)


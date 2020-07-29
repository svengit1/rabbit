import pyglet

from map_objects.map_entity import MapEntity
from resources import segment_height, segment_width
import random

class Sea(MapEntity):
    def __init__(self, **kwargs):
        self.width = kwargs['width']
        self.depth = kwargs['depth']
        self.image = Sea.create_image(self.width, self.depth)
        self.x = kwargs['hpos'] * segment_width
        self.y = kwargs['vpos'] * segment_height

    @staticmethod
    def create_image(width, depth):
        u = [74 for i in range(1, 100)]
        for i in range(10):
            u[random.randint(0, 99)] = 73
        image = pyglet.image.Texture.create(width * segment_width, depth * segment_height)
        for w in range(width):
            image = Sea.add_image(image, 85, w * segment_width, (depth - 1) * segment_height)
            for d in range(0, depth - 1):
                image = Sea.add_image(image, random.choice(u), w * segment_width, d * segment_height)
        return image
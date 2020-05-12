import pyglet

from map_objects.map_entity import MapEntity
from resources import segment_height, segment_width


class SmallTree(MapEntity):
    def __init__(self, **kwargs):
        self.image = SmallTree.create_image()
        self.x = kwargs['hpos'] * segment_width
        self.y = kwargs['vpos'] * segment_height

    @staticmethod
    def create_image():
        width = 2
        height = 2
        image = pyglet.image.Texture.create(width * segment_width,
                                            height * segment_height)
        image = SmallTree.add_images(image, (51, 0, 32), (52, 32, 32),
                                     (39, 0, 0), (40, 32, 0))
        return image

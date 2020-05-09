import pyglet
from game.map_entity import MapEntity
from game.resources import segment_height, segment_width


class Cloud(MapEntity):
    def __init__(self):
        self.image = Cloud.create_image()

    @staticmethod
    def create_image():
        width = 5
        height = 2
        image = pyglet.image.Texture.create(width * segment_width,
                                            height * segment_height)
        image = Cloud.add_images(image, (1, 0, 0), (2, 32, 0), (3, 64, 0),
                                 (4, 96, 0), (5, 128, 0), (13, 0, 32),
                                 (14, 32, 32), (15, 64, 32), (16, 96, 32))

        return image

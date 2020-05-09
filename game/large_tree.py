import pyglet
from game.map_entity import MapEntity
from game.resources import segment_height, segment_width


class LargeTree(MapEntity):
    def __init__(self):
        self.image = LargeTree.create_image()

    @staticmethod
    def create_image():
        width = 3
        height = 3
        image = pyglet.image.Texture.create(width * segment_width,
                                            height * segment_height)
        LargeTree.add_images(image, (41, 0, 0), (42, 32, 0), (43, 64, 0),
                             (53, 0, 32), (54, 32, 32), (55, 64, 32),
                             (65, 0, 64), (66, 32, 64), (67, 64, 64))
        return image

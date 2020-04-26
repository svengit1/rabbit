from game.resources import segment_height, segment_width
import pyglet
from game.map_entity import MapEntity


class LargeTree(MapEntity):
    def __init__(self):
        self.image = LargeTree.create_image()

    @staticmethod
    def create_image():
        width = 3
        height = 3
        image = pyglet.image.Texture.create(width * segment_width, height * segment_height)
        image = LargeTree.add_image(image, 41, 0, 0)
        image = LargeTree.add_image(image, 42, 32, 0)
        image = LargeTree.add_image(image, 43, 64, 0)
        image = LargeTree.add_image(image, 53, 0, 32)
        image = LargeTree.add_image(image, 54, 32, 32)
        image = LargeTree.add_image(image, 55, 64, 32)
        image = LargeTree.add_image(image, 65, 0, 64)
        image = LargeTree.add_image(image, 66, 32, 64)
        image = LargeTree.add_image(image, 67, 64, 64)

        return image

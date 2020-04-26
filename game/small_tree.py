from game.map_entity import MapEntity
from game.resources import segment_width, segment_height
import pyglet


class SmallTree(MapEntity):
    def __init__(self):
        self.image = SmallTree.create_image()

    @staticmethod
    def create_image():
        width = 2
        height = 2
        image = pyglet.image.Texture.create(width * segment_width, height * segment_height)
        image = SmallTree.add_image(image, 51, 0, 32)
        image = SmallTree.add_image(image, 52, 32, 32)
        image = SmallTree.add_image(image, 39, 0, 0)
        image = SmallTree.add_image(image, 40, 32, 0)

        return image



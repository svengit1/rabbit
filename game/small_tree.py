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
        image = SmallTree.add_images(image, (51, 0, 32), (52, 32, 32), (39, 0, 0), (40, 32,0))
        return image



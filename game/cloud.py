from game.resources import segment_width, segment_height
import pyglet
from game.map_entity import MapEntity


class Cloud(MapEntity):
    def __init__(self):
        self.image = Cloud.create_image()

    @staticmethod
    def create_image():
        width = 5
        height = 2
        image = pyglet.image.Texture.create(width * segment_width, height * segment_height)
        image = Cloud.add_image(image, 1, 0, 0)
        image = Cloud.add_image(image, 2, 32, 0)
        image = Cloud.add_image(image, 3, 64, 0)
        image = Cloud.add_image(image, 4, 96, 0)
        image = Cloud.add_image(image, 5, 128, 0)
        image = Cloud.add_image(image, 13, 0, 32)
        image = Cloud.add_image(image, 14, 32, 32)
        image = Cloud.add_image(image, 15, 64, 32)
        image = Cloud.add_image(image, 16, 96, 32)

        return image
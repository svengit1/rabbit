from game.resources import map_images
import pyglet
import pyglet.gl as gl


class LargeTree:
    def __init__(self):
        self.segment_width = 32
        self.segment_height = 32
        self.image = LargeTree.create_image()

    @staticmethod
    def add_image(image, id, x, y):
        image.blit_into(map_images[id].get_image_data(), x, y, 0)
        return image

    @staticmethod
    def create_image():
        width = 3
        height = 3
        image = pyglet.image.Texture.create(width * 32, height * 32)
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

    def draw(self, **kwargs):
        y = kwargs['vpos']*self.segment_height
        x = kwargs['hpos']*self.segment_width
        gl.glEnable(gl.GL_BLEND)
        self.image.blit(x, y)


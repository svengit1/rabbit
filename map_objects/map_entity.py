import pyglet.gl as gl

from resources import map_images, segment_height, segment_width


class MapEntity:
    @staticmethod
    def add_image(image, image_id, x, y):
        image.blit_into(map_images[image_id].get_image_data(), x, y, 0)
        return image

    @staticmethod
    def add_images(image, *args):
        for img in args:
            image = MapEntity.add_image(image, img[0], img[1], img[2])
        return image

    def draw_on_position(self, **kwargs):
        y = kwargs['vpos'] * segment_height
        x = kwargs['hpos'] * segment_width
        gl.glEnable(gl.GL_BLEND)
        self.image.blit(x, y)

    def draw(self):
        gl.glEnable(gl.GL_BLEND)
        self.image.blit(self.x, self.y)

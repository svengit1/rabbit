from game.resources import map_images
import pyglet.gl as gl


class Bush:
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.image = map_images[38].get_image_data()
        self.segment_height = 32
        self.segment_width = 32

    def draw(self, **kwargs):
        y = kwargs['vpos']*self.segment_height
        x = kwargs['hpos']*self.segment_width
        gl.glEnable(gl.GL_BLEND)
        self.image.blit(x, y)


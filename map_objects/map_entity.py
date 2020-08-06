import pyglet.gl as gl
import pymunk

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

    @staticmethod
    def get_origin(platform_levels):
        xs = [i[0] for i in platform_levels]
        ys = [i[1] for i in platform_levels]
        origin = (min(xs), min(ys))
        return origin

    @staticmethod
    def translate_block(platform_levels):
        origin = MapEntity.get_origin(platform_levels)
        vs = map(lambda k: (k[0]-origin[0], k[1]-origin[1]), platform_levels)
        return vs

    @staticmethod
    def scale_block(platform_levels):
        vs = map(lambda k: (k[0] * segment_width, k[1] * segment_height), platform_levels)
        return vs

    @staticmethod
    def get_shapes(body, args):
        shapes = []
        k = [sum(i) for i in args]
        origin = args[k.index(min(k))]
        counter = 0
        # print(args)
        for vertices in args:
            counter += 1
            if counter == len(args):
                counter = 0
            vs = [(vertices[0] * segment_width, origin[1] * segment_height),
                  (vertices[0] * segment_width, args[counter][1] * segment_height),
                  ((args[counter][0] + 1) * segment_width, args[counter][1] * segment_height),
                  ((args[counter][0] + 1) * segment_width, origin[1] * segment_height)]
            shape = pymunk.Poly(body, vs)
            shape.friction = 4.0
            shape.elasticity = 0
            shape.collision_type = 3
            shapes.append(shape)
        return shapes

    def draw_on_position(self, **kwargs):
        y = kwargs['vpos'] * segment_height
        x = kwargs['hpos'] * segment_width
        gl.glEnable(gl.GL_BLEND)
        self.image.blit(x, y)

    def draw(self):
        gl.glEnable(gl.GL_BLEND)
        self.image.blit(self.x, self.y)

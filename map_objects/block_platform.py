import pyglet
import pymunk
from pymunk.body import Body

import resources
import random
from map_objects.map_entity import MapEntity
from resources import segment_height, segment_width
from pyglet.gl import *


class BlockPlatform(MapEntity):
    BLOCK_PLATFORM_LTOP = pyglet.resource.image("tile-1s.png")
    BLOCK_PLATFORM_TOP = pyglet.resource.image('tile-2s.png')
    BLOCK_PLATFORM_RTOP = pyglet.resource.image('tile-3s.png')
    BLOCK_PLATFORM_LE = pyglet.resource.image('tile-4s.png')
    BLOCK_PLATFORM_F = pyglet.resource.image('tile-5s.png')
    BLOCK_PLATFORM_RE = pyglet.resource.image('tile-6s.png')
    BLOCK_PLATFORM_UPRC = pyglet.resource.image('tile-7s.png')
    BLOCK_PLATFORM_FCL = pyglet.resource.image('tile-8s.png')
    BLOCK_PLATFORM_BOTTOM = pyglet.resource.image('tile-9s.png')
    BLOCK_PLATFORM_FCR = pyglet.resource.image('tile-10s.png')
    BLOCK_PLATFORM_UPLC = pyglet.resource.image('tile-11s.png')
    BLOCK_PLATFORM_BLC = pyglet.resource.image('tile-12s.png')
    BLOCK_PLATFORM_BRC = pyglet.resource.image('tile-13s.png')
    BLOCK_PLATFORM_BONES = [pyglet.resource.image('bone-bg-1.png'),
                            pyglet.resource.image('bone-bg-2.png'),
                            pyglet.resource.image('bone-bg-3.png'),
                            pyglet.resource.image('bone-bg-4.png')]

    def __init__(self, *args, **kwargs):
        self.space = kwargs['space']
        self.__init_physics(args)
        self.image = self.create_image(args)

    def __init_physics(self, args):
        self.body = pymunk.Body(mass=0, moment=0, body_type=Body.KINEMATIC)
        self.shps = MapEntity.get_shapes(self.body, args)
        self.body.player_on_the_platform = False
        self.space.add(self.body)
        self.space.add(self.shps)
        origin = MapEntity.get_origin(args)
        self.x, self.y = origin[0] * segment_width, origin[1] * segment_height

    @staticmethod
    def get_image(scaled_translated_levels, x, y, background=True):
        n = len(scaled_translated_levels)
        cnt = 0
        for s in scaled_translated_levels:
            cnt += 1
            if cnt == n:
                cnt = 0
            if s[0] < x <= scaled_translated_levels[cnt][0] and scaled_translated_levels[cnt][1] > y and background:
                if random.randrange(1, 100) < 5:
                    container_bg_image = pyglet.image.Texture.create(resources.segment_width, resources.segment_height)
                    container_bg_image.blit_into(BlockPlatform.BLOCK_PLATFORM_F.get_image_data(), 0, 0, 0)
                    glEnable(GL_BLEND)
                    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                    container_bg_image.blit_into(random.choice(BlockPlatform.BLOCK_PLATFORM_BONES).get_image_data(), 0, 0, 0)
                    return container_bg_image
                return BlockPlatform.BLOCK_PLATFORM_F

            if x == scaled_translated_levels[-1][0] and y == 0:
                return BlockPlatform.BLOCK_PLATFORM_BRC
            elif x == 0 and y == 0:
                return BlockPlatform.BLOCK_PLATFORM_BLC
            elif s[1] - segment_height < y < scaled_translated_levels[cnt][1] - segment_height and x == s[0]:
                return BlockPlatform.BLOCK_PLATFORM_LE
            elif s[1] - segment_height > y > scaled_translated_levels[cnt][1] - segment_height and x == s[0]:
                return BlockPlatform.BLOCK_PLATFORM_RE
            elif y == 0 and x < scaled_translated_levels[-1][0]:
                return BlockPlatform.BLOCK_PLATFORM_BOTTOM
            elif y == s[1] - segment_height:
                if s[0] - segment_width == x and s[1] < scaled_translated_levels[cnt][1]:
                    return BlockPlatform.BLOCK_PLATFORM_UPRC
                elif scaled_translated_levels[cnt - 2][0] + segment_width == x and s[1] < \
                        scaled_translated_levels[cnt - 2][1]:
                    return BlockPlatform.BLOCK_PLATFORM_UPLC
                elif scaled_translated_levels[cnt - 2][0] == x and s[1] > scaled_translated_levels[cnt - 2][1]:
                    return BlockPlatform.BLOCK_PLATFORM_LTOP
                elif s[0] > x > scaled_translated_levels[cnt - 2][0]:
                    return BlockPlatform.BLOCK_PLATFORM_TOP
                elif s[0] == x and s[1] > scaled_translated_levels[cnt][1]:
                    return BlockPlatform.BLOCK_PLATFORM_RTOP
                elif scaled_translated_levels[cnt - 2][0] == x and s[1] < scaled_translated_levels[cnt - 2][1]:
                    return BlockPlatform.BLOCK_PLATFORM_FCR
                elif s[0] == x and s[1] < scaled_translated_levels[cnt][1]:
                    return BlockPlatform.BLOCK_PLATFORM_FCL

    @staticmethod
    def container_blit(container, scaled_translated_levels, width, height, background):
        for x in range(0, (width + 1) * resources.segment_width, resources.segment_width):
            for y in range(0, (height + 1) * resources.segment_height, resources.segment_height):
                im = BlockPlatform.get_image(scaled_translated_levels, x, y, background=background)
                if im:
                    container.blit_into(im.get_image_data(), x, y, 0)
        return container

    @staticmethod
    def get_bounding_box(args):
        x_coordinates = []
        y_coordinates = []
        for i in range(len(args)):
            x_coordinates.append(list(args)[i][0])
            y_coordinates.append(list(args)[i][1])

        width = max(x_coordinates) - min(x_coordinates)
        height = max(y_coordinates) - min(y_coordinates)
        return width, height

    @staticmethod
    def create_image(args):
        width, height = BlockPlatform.get_bounding_box(args)

        container_image = pyglet.image.Texture.create((width + 1) * resources.segment_width,
                                                      (height + 1) * resources.segment_height)

        scaled_translated_levels = list(MapEntity.scale_block(MapEntity.translate_block(args)))

        container_image = BlockPlatform.container_blit(container_image, scaled_translated_levels, width, height, True)
        container_image = BlockPlatform.container_blit(container_image, scaled_translated_levels, width, height, False)

        return container_image

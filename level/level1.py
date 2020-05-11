import pyglet
import pyglet.gl as gl

from collectables.fruit import Fruit
from map_objects.bridge import Bridge
from map_objects.bush import Bush
from map_objects.cloud import Cloud
from map_objects.large_tree import LargeTree
from map_objects.moving_platform import MovingPlatform
from map_objects.platform import Platform
from map_objects.small_tree import SmallTree


class Level1:
    def __init__(self, space, world_batch, background):
        self.p10 = Platform(space=space, hpos=0, vpos=15, width=10)
        self.p8 = Platform(space=space, hpos=16, vpos=15, width=8)
        self.bridge = Bridge(space=space, hpos=8, vpos=16, width=10)
        self.p6 = Platform(space=space, hpos=25, vpos=17, width=6)
        self.p10a = Platform(space=space, hpos=32, vpos=15, width=10)
        self.grape = Fruit(space=space,
                           type=Fruit.GRAPE,
                           points=10,
                           hpos=9,
                           vpos=19,
                           batch=world_batch,
                           group=background)
        self.lemon = Fruit(space=space,
                           type=Fruit.LEMON,
                           points=20,
                           hpos=13,
                           vpos=20,
                           batch=world_batch,
                           group=background)
        self.carrot = Fruit(space=space,
                            type=Fruit.CARROT,
                            points=30,
                            hpos=15,
                            vpos=19,
                            batch=world_batch,
                            group=background)

        self.moving_platform3 = MovingPlatform(space=space,
                                               width=20,
                                               initial_position=(35, 10),
                                               velocity=(150, 19),
                                               path_length=500,
                                               batch=world_batch,
                                               group=background)

        self.large_tree = LargeTree()
        self.bush = Bush()
        self.cloud = Cloud()
        self.small_tree = SmallTree()

    def update(self, dt):
        self.moving_platform3.update(dt)

    def draw(self):
        self.p10.draw()
        self.p8.draw()
        self.p6.draw()
        self.p10a.draw()
        self.large_tree.draw_on_position(hpos=27, vpos=18)
        self.bush.draw_on_position(hpos=4, vpos=16)
        self.cloud.draw_on_position(hpos=20, vpos=23)
        self.cloud.draw_on_position(hpos=8, vpos=21)
        self.small_tree.draw_on_position(hpos=5, vpos=16)
        self.bridge.draw()

        for seg in self.bridge.lines:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                 ('v2f', (seg.a.x, seg.a.y, seg.b.x, seg.b.y)))

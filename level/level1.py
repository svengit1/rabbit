import pyglet
import pyglet.gl as gl
from collectables.collectable import Collectable
from collectables.fruit import Fruit
from map_objects.sea import Sea
from collectables.level_end import LevelEnd
from enemy.enemy import Enemy
from level.base_level import BaseLevel
from map_objects.bridge import Bridge
from map_objects.bush import Bush
from map_objects.cloud import Cloud
from map_objects.large_tree import LargeTree
from map_objects.moving_platform import MovingPlatform
from map_objects.platform import Platform
from map_objects.small_tree import SmallTree
from map_objects.scenery_decoration import SceneryDecoration
from map_objects.spring import Spring
from map_objects.block_platform import BlockPlatform


class Level1(BaseLevel):
    def __init__(self, game):
        super().__init__(game)

    def create(self, space, background):
        # p = Platform(space=space, hpos=16, vpos=15, width=8)
        # u = Platform(space=space, hpos=46, vpos=17, width=5)
        # b = BlockPlatform((76, 1), (83, 4), (99, 6), (102, 7), (107, 8), space=space)
        self.add_to_scenery(
            BlockPlatform((0, 0), (12, 7), (17, 5), space=space),
            MovingPlatform(space=space,
                           width=8,
                           initial_position=(18, 7),
                           velocity=(50, 100),
                           path_length=275,
                           group=background),
            BlockPlatform((26, 0), (30, 5), (35, 7), (45, 5), space=space),
            BlockPlatform((30, 14), (34, 17), (46, 19),  space=space),
            BlockPlatform((54, 14), (58, 16), (65, 17), space=space),
            MovingPlatform(space=space,
                           width=4,
                           initial_position=(47, 6),
                           velocity=(0, 100),
                           path_length=125,
                           group=background),
            MovingPlatform(space=space,
                           width=4,
                           initial_position=(56, 7),
                           velocity=(0, 128),
                           path_length=125,
                           group=background),
            MovingPlatform(space=space,
                           width=4,
                           initial_position=(63, 6),
                           velocity=(0, 125),
                           path_length=125,
                           group=background),
            MovingPlatform(space=space,
                           width=4,
                           initial_position=(71, 4),
                           velocity=(0, 100),
                           path_length=125,
                           group=background),
            MovingPlatform(space=space,
                           width=8,
                           initial_position=(80, 2),
                           velocity=(80, 110),
                           path_length=475,
                           group=background),
            SceneryDecoration(hpos=1, vpos=7, type=SceneryDecoration.CRATE),
            SceneryDecoration(hpos=2, vpos=7, type=SceneryDecoration.CRATE),
            SceneryDecoration(hpos=3, vpos=7, type=SceneryDecoration.CRATE),
            SceneryDecoration(hpos=1, vpos=8, type=SceneryDecoration.CRATE),
            SceneryDecoration(hpos=2, vpos=8, type=SceneryDecoration.CRATE),
            SceneryDecoration(hpos=5, vpos=7, type=SceneryDecoration.SIGN),

        )


# Platform(space=space, hpos=0, vpos=15, width=10), p, b,
# Bridge(space=space, hpos=9, vpos=15, width=8),
# Platform(space=space, hpos=25, vpos=17, width=6),
# Platform(space=space, hpos=32, vpos=15, width=10), u,
# Platform(space=space, hpos=50, vpos=14, width=7),
# Platform(space=space, hpos=49, vpos=11, width=19),
# Spring(space=space, hpos=73, vpos=4),
# Sea(space=space, hpos=0, vpos=0, width=80, depth=4),
# LargeTree(hpos=27, vpos=18),
# Cloud(hpos=20, vpos=23), Cloud(hpos=8, vpos=21),
# SceneryDecoration(hpos=6, vpos=16, type=SceneryDecoration.SKELETON),
            # SceneryDecoration(hpos=34, vpos=16, type=SceneryDecoration.TOMBSTONE_CROSS),
            # SceneryDecoration(hpos=23, vpos=16, type=SceneryDecoration.ARROWSIGN),
            # SceneryDecoration(hpos=17, vpos=16, type=SceneryDecoration.SIGN),
            # SceneryDecoration(hpos=16, vpos=16, type=SceneryDecoration.BUSH),
            # SceneryDecoration(hpos=15, vpos=16, type=SceneryDecoration.DEAD_BUSH),
            # SceneryDecoration(hpos=14, vpos=16, type=SceneryDecoration.DEAD_TREE),
            # Fruit(space=space,
            #       type=Fruit.PURPLE_GRAPE,
            #       points=10,
            #       hpos=9,
            #       vpos=19,
            #       group=background),
            # Fruit(space=space,
            #       type=Fruit.STRAWBERRY,
            #       points=10,
            #       hpos=10,
            #       vpos=19,
            #       group=background),
            # Fruit(space=space,
            #       type=Fruit.MELLON,
            #       points=10,
            #       hpos=11,
            #       vpos=19,
            #       group=background),
            # Fruit(space=space,
            #       type=Fruit.ORANGE,
            #       points=10,
            #       hpos=12,
            #       vpos=19,
            #       group=background),
            # Fruit(space=space,
            #       type=Fruit.RED_APPLE,
            #       points=10,
            #       hpos=13,
            #       vpos=19,
            #       group=background),
            #
            # Fruit(space=space,
            #       type=Fruit.GREEN_GRAPE,
            #       points=10,
            #       hpos=14,
            #       vpos=19,
            #       group=background),
            # Fruit(space=space,
            #       type=Fruit.LEMON,
            #       points=20,
            #       hpos=15,
            #       vpos=20,
            #       group=background),
            # Fruit(space=space,
            #       type=Fruit.CARROT,
            #       points=30,
            #       hpos=16,
            #       vpos=19,
            #       group=background), # LevelEnd(space=space, hpos=105, vpos=16),
            # Enemy(initial_position=(80, 4), space=space, level=1),


        # self.add_to_scenery(Enemy.guards(p, background, 1))
        # self.add_to_scenery(Enemy.guards(u, background, 1))
        #self.add_to_scenery(Enemy.guards(b, background, 1))


        # self.add_to_scenery(*[
        #     Enemy.guards(i, background, self) for i in list(
        #         filter(
        #             lambda p: isinstance(p, Platform) or isinstance(
        #                 p, MovingPlatform), self.scenery))
        # ])

    def update(self, dt):
        super().update(dt)

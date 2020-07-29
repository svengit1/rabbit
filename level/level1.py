import pyglet
import pyglet.gl as gl

from collectables.collectable import Collectable
from collectables.fruit import Fruit
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
from map_objects.spring import Spring


class Level1(BaseLevel):
    def __init__(self, game):
        super().__init__(game)

    def create(self, space, background):
        p = Platform(space=space, hpos=16, vpos=15, width=8)
        self.add_to_scenery(
            Platform(space=space, hpos=0, vpos=15, width=10), p,
            Bridge(space=space, hpos=8, vpos=15, width=10),
            Platform(space=space, hpos=25, vpos=17, width=6),
            Platform(space=space, hpos=32, vpos=15, width=10),
            LargeTree(hpos=27, vpos=18), Bush(hpos=4, vpos=16),
            Cloud(hpos=20, vpos=23), Cloud(hpos=8, vpos=21),
            SmallTree(hpos=5, vpos=16),
            Fruit(space=space,
                  type=Fruit.GRAPE,
                  points=10,
                  hpos=9,
                  vpos=19,
                  group=background),
            Fruit(space=space,
                  type=Fruit.LEMON,
                  points=20,
                  hpos=13,
                  vpos=20,
                  group=background),
            Fruit(space=space,
                  type=Fruit.CARROT,
                  points=30,
                  hpos=15,
                  vpos=19,
                  group=background), LevelEnd(space=space, hpos=50, vpos=17),
            MovingPlatform(space=space,
                           width=20,
                           initial_position=(10, 5),
                           velocity=(150, 19),
                           path_length=500,
                           group=background))

        #        self.add_to_scenery(Enemy.gards(p, background))

        self.add_to_scenery(*[
            Enemy.guards(i, background, self) for i in list(
                filter(
                    lambda p: isinstance(p, Platform) or isinstance(
                        p, MovingPlatform), self.scenery))
        ])

    def update(self, dt):
        super().update(dt)

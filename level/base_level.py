import itertools

import pyglet

from collectables.collectable import Collectable
from map_objects.map_entity import MapEntity
from map_objects.platform import Platform


def draw_debug_box(shape, body):
    ps = shape.get_vertices()
    ps = [p.rotated(body.angle) + body.position for p in ps]
    n = len(ps)
    ps = [c for p in ps for c in p]
    pyglet.graphics.draw(n, pyglet.gl.GL_LINE_LOOP, ('v2f', ps),
                         ('c3f', (1, 0, 0) * n))


class BaseLevel:
    def __init__(self, game):
        self.scenery = []
        self.game = game

    @staticmethod
    def __filter_has_update__(level_elements):
        return filter(lambda x: callable(getattr(x, "update", None)),
                      level_elements)

    def add_to_scenery(self, *map_objects):
        self.scenery.extend(map_objects)

    def draw(self):
        for s in self.scenery:
            s.draw()

    def update(self, dt):
        for x in list(self.__filter_has_update__(self.scenery)):
            x.update(dt)

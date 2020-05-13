import pyglet
from map_objects.platform import Platform
from collectables.collectable import Collectable
from map_objects.map_entity import MapEntity


def draw_debug_box(shape, body):
    ps = shape.get_vertices()
    ps = [p.rotated(body.angle) + body.position for p in ps]
    n = len(ps)
    ps = [c for p in ps for c in p]
    pyglet.graphics.draw(n, pyglet.gl.GL_LINE_LOOP, ('v2f', ps),
                         ('c3f', (1, 0, 0) * n))


class BaseLevel:
    def __init__(self):
        self.scenery = []

    def store(self, *map_objects):
        self.scenery.extend(map_objects)

    def solved(self):
        raise NotImplementedError

    def draw(self):
        for s in self.scenery:
            s.draw()
            if isinstance(s, Platform):
                draw_debug_box(s.shape, s.body)

    def update(self, dt):
        for x in list(
                filter(lambda j: isinstance(j, Collectable), self.scenery)):
            x.update(dt)

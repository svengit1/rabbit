import pyglet
import pyglet.gl as gl
import pymunk
from pygame.sprite import Sprite
from pyglet.window import FPSDisplay
from pymunk import Vec2d

from collectables.collectable import Collectable
from collectables.fruit import Fruit


class BaseLevel:
    def __init__(self):
        self.scenery = []

    def store(self, *map_objects):
        self.scenery.extend(map_objects)

    def solved(self):
        raise NotImplementedError

    def draw_debug_box(self, sprite):
        ps = sprite.shape.get_vertices()
        ps = [p.rotated(sprite.body.angle) + sprite.body.position for p in ps]
        n = len(ps)
        ps = [c for p in ps for c in p]
        pyglet.graphics.draw(n, pyglet.gl.GL_LINE_LOOP, ('v2f', ps),
                             ('c3f', (1, 0, 0) * n))

    def draw(self):
        for s in self.scenery:
            s.draw()

    def update(self, dt):
        for x in list(
                filter(lambda j: isinstance(j, Collectable), self.scenery)):
            x.update(dt)

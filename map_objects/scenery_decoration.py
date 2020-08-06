import pyglet
from map_objects.map_entity import MapEntity
from resources import segment_height, segment_width


class SceneryDecoration(MapEntity):
    SKELETON = pyglet.resource.image('skeleton-s.png')
    BUSH = pyglet.resource.image('bush-1.png')
    DEAD_BUSH = pyglet.resource.image('deadbush.png')
    TOMBSTONE = pyglet.resource.image('tombstone-1s.png')
    TOMBSTONE_CROSS = pyglet.resource.image('tombstone-2s.png')
    SIGN = pyglet.resource.image('sign-s.png')
    ARROWSIGN = pyglet.resource.image('arrowsign-s.png')
    CRATE = pyglet.resource.image('crate-s.png')
    DEAD_TREE = pyglet.resource.image('tree-s.png')

    def __init__(self, **kwargs):
        self.image = kwargs['type']
        self.x = kwargs['hpos'] * segment_width
        self.y = kwargs['vpos'] * segment_height

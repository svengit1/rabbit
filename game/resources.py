import pyglet


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


segment_width = 32
segment_height = 32

window_width = 960
window_height = 832

state = dict()
state['screen_pan_x'] = 0
state['score'] = 0

# Tell pyglet where to find the resources
pyglet.resource.path = [
    './resources', './resources/map_art', './resources/player'
]
pyglet.resource.reindex()

# Load the three main resources and get them to draw centered
tile_ground_left = pyglet.resource.image("tile-ground-left.png")

tile_ground = pyglet.resource.image("tile-ground.png")

tile_ground_right = pyglet.resource.image("tile-ground-right.png")

stone_platform_left = pyglet.resource.image("stone-platform-left.png")

stone_platform_middle = pyglet.resource.image("stone-platform-middle.png")

stone_platform_right = pyglet.resource.image("stone-platform-right.png")

map_segments_image = pyglet.resource.image("tiles.png")

map_images = pyglet.image.ImageGrid(map_segments_image, 19, 12)

rabbit_image_segments = pyglet.resource.image('player.png')

rabbit_images = pyglet.image.ImageGrid(rabbit_image_segments, 64, 1)

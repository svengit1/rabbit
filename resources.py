import pyglet


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


segment_width = 32
segment_height = 32

window_width = 1280
window_height = int(window_width / 1.749)

state = dict()
state = {'screen_pan_x': 0, 'score': 0, 'lives': 3, 'level': 0}
last_level = 1

# Tell pyglet where to find the resources
pyglet.resource.path = [
    './images', './images/map_art', './images/player',
    './images/graveyard/png', './images/enemies/male',
    './images/enemies/female'
]
pyglet.resource.reindex()

# Load the three main resources and get them to draw centered
background_image = pyglet.resource.image("bg.png")
background_image.width = window_width
background_image.height = window_height
map_segments_image = pyglet.resource.image("tiles.png")

map_images = pyglet.image.ImageGrid(map_segments_image, 19, 12)

rabbit_image_segments = pyglet.resource.image('player.png')

player_image = pyglet.resource.image('qb7e6.png')

rabbit_images = pyglet.image.ImageGrid(rabbit_image_segments, 64, 1)

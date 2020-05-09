import pyglet as pyglet
import pyglet.gl as gl
import pymunk
from pyglet.window import FPSDisplay
from pymunk import Vec2d

from game.bridge import Bridge
from game.bush import Bush
from game.cloud import Cloud
from game.collectables.fruit import Fruit
from game.large_tree import LargeTree
from game.moving_platform import MovingPlatform
from game.platform import Platform
from game.player.rabbit import Rabbit
from game.resources import state, window_height, window_width
from game.small_tree import SmallTree

window = pyglet.window.Window(window_width, window_height)
background_colour = pyglet.image.SolidColorImagePattern((143, 187, 247, 255)).\
    create_image(window_width, window_height)

world_batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)

score_label = pyglet.text.Label(text="Score: 0",
                                x=10,
                                y=800,
                                font_size=24,
                                bold=True,
                                color=(255, 255, 255, 255))

# Physics stuff
space = pymunk.Space()
space.gravity = Vec2d(0.0, -1200.0)

p10 = Platform(space=space, hpos=0, vpos=15, width=10)
p8 = Platform(space=space, hpos=16, vpos=15, width=8)
bridge = Bridge(space=space, hpos=8, vpos=16, width=10)
p6 = Platform(space=space, hpos=25, vpos=17, width=6)
p10a = Platform(space=space, hpos=32, vpos=15, width=10)
grape = Fruit(space=space,
              type=Fruit.GRAPE,
              points=10,
              hpos=9,
              vpos=19,
              batch=world_batch,
              group=background)
lemon = Fruit(space=space,
              type=Fruit.LEMON,
              points=20,
              hpos=13,
              vpos=20,
              batch=world_batch,
              group=background)
carrot = Fruit(space=space,
               type=Fruit.CARROT,
               points=30,
               hpos=15,
               vpos=19,
               batch=world_batch,
               group=background)
moving_platform3 = MovingPlatform(space=space,
                                  width=20,
                                  initial_position=(35, 10),
                                  velocity=(150, 19),
                                  path_length=500,
                                  batch=world_batch,
                                  group=background)

large_tree = LargeTree()
rabbit = Rabbit(x=100, y=600, batch=world_batch, group=background, space=space)
bush = Bush()
cloud = Cloud()
small_tree = SmallTree()

window.push_handlers(rabbit.key_handler)

fps_display = FPSDisplay(window)


def sticky_draw(obj, win):
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glPushMatrix()
    gl.glLoadIdentity()
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glPushMatrix()
    gl.glLoadIdentity()
    gl.glOrtho(0, win.width, 0, win.height, -1, 1)
    obj.draw()
    gl.glPopMatrix()
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glPopMatrix()


def draw_debug_box(sprite):
    ps = sprite.shape.get_vertices()
    ps = [p.rotated(sprite.body.angle) + sprite.body.position for p in ps]
    n = len(ps)
    ps = [c for p in ps for c in p]
    pyglet.graphics.draw(n, pyglet.gl.GL_LINE_LOOP, ('v2f', ps),
                         ('c3f', (1, 0, 0) * n))


def update_score_label():
    score_label.text = "Score: " + str(state['score'])


@window.event
def on_draw():
    window.clear()
    background_colour.blit(state['screen_pan_x'], 0)
    p10.draw()
    p8.draw()
    p6.draw()
    p10a.draw()
    large_tree.draw_on_position(hpos=27, vpos=18)
    bush.draw_on_position(hpos=4, vpos=16)
    cloud.draw_on_position(hpos=20, vpos=23)
    cloud.draw_on_position(hpos=8, vpos=21)
    small_tree.draw_on_position(hpos=5, vpos=16)
    bridge.draw()
    world_batch.draw()

    # draw_debug_box(rabbit)
    #draw_debug_box(carrot)
    #draw_debug_box(moving_platform)
    #draw_debug_box(p10)
    for seg in bridge.lines:
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                             ('v2f', (seg.a.x, seg.a.y, seg.b.x, seg.b.y)))

    fps_display.draw()

    sticky_draw(score_label, window)


def update(dt):
    dt = 1.0 / 120.
    space.step(dt)
    rabbit.update(dt)
    #moving_platform1.update(dt)
    #moving_platform2.update(dt)
    moving_platform3.update(dt)
    update_score_label()


if __name__ == "__main__":
    # Start it up!
    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()

import pyglet as pyglet
from pyglet.window import FPSDisplay
from game.platform import Platform
from game.small_tree import SmallTree
from game.large_tree import LargeTree
from game.bush import Bush
from game.cloud import Cloud
from game.bridge import Bridge
from game.resources import rabbit_images
from game.rabbit import Rabbit
import pymunk
from pymunk import Vec2d
from pyglet.gl import glTranslatef
import pyglet.gl as gl

from pyglet.window import key

window_width = 960
window_height = 832


window = pyglet.window.Window(window_width, window_height)
world_batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)

score_label = pyglet.text.Label(text="Score: 0",
                                x=10, y=800,
                                font_size=24, bold=True,
                                color=(200, 200, 200, 200))


# Physics stuff
space = pymunk.Space()
space.gravity = Vec2d(0.0, -900.0)


p10 = Platform(space=space, hpos=0, vpos=15, width=10)
p8 = Platform(space=space, hpos=16, vpos=15, width=8)
b1 = Bridge(window=window, batch=world_batch, group=background, space=space)
b1.create(hpos=8, vpos=16, size=10)
p6 = Platform(space=space, hpos=25, vpos=17, width=6)
p10a = Platform(space=space, hpos=32, vpos=15, width=10)

t1 = LargeTree(window=window, batch=world_batch, group=background)
t1.create(hpos=27, vpos=18)

rabbit = Rabbit(x=100, y=600, batch=world_batch, group=background, space=space)


# t1 = SmallTree(window=window, batch=world_batch, group=background)
# t1.create(hpos=5, vpos=1)
#
# t2 = LargeTree(window=window, batch=world_batch, group=background)
# t2.create(hpos=15, vpos=10)
#
# b1 = Bush(window=window, batch=world_batch, group=background)
# b1.create(hpos=11, vpos=12)
#
# c1 = Cloud(window=window, batch=world_batch, group=background)
# c1.create(hpos=20, vpos=15)


#t1 = SmallTree(window=window, batch=world_batch, group=background)
#t1.create(hpos=7, vpos=6)

#t1 = SmallTree(window=window, batch=world_batch, group=background)
#t1.create(hpos=11, vpos=7)

# g2 = Bridge(window=window, batch=world_batch, group=background)
# g2.create(hpos=0, vpos=2, size=20)

window.push_handlers(rabbit.key_handler)

keys = key.KeyStateHandler()

window.push_handlers(keys)

fps_display = FPSDisplay(window)

def movement(keys):
    if keys[key.I]:
        glTranslatef(0,10,0)
    if keys[key.K]:
        glTranslatef(0,-10,0)
    if keys[key.J]:
        glTranslatef(-10,0,0)
    if keys[key.L]:
        glTranslatef(10,0,0)


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


        
def init():
    global score


    score = 0
    score_label.text = "Score: " + str(score)


@window.event
def on_draw():
    window.clear()
    world_batch.draw()
    p10.draw()
    p8.draw()
    p6.draw()
    p10a.draw()
    

    ps = rabbit.shape.get_vertices()
    ps = [p.rotated(rabbit.body.angle) + rabbit.body.position for p in ps]
    n = len(ps)
    ps = [c for p in ps for c in p]
    pyglet.graphics.draw(n, pyglet.gl.GL_LINE_LOOP,
             ('v2f', ps), ('c3f', (1, 0, 0)*n))

    for seg in b1.lines:
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (seg.a.x, seg.a.y, seg.b.x, seg.b.y)))

    fps_display.draw()

    sticky_draw(score_label, window)



def update(dt):
    global score
    dt = 1.0/120.
    space.step(dt)
    rabbit.update(dt)
    movement(keys)


if __name__ == "__main__":
    # Start it up!
    init()
    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()

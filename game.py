import pyglet as pyglet
import pyglet.gl as gl
import pymunk
from pyglet.window import FPSDisplay
from pymunk import Vec2d

from level.level1 import Level1
from level.level2 import Level2
from level.level3 import Level3

from player.rabbit import Rabbit
from resources import state, window_height, window_width


class Game:
    def __init__(self, window):
        self.window = window
        self.background_colour = pyglet.image.SolidColorImagePattern((143, 187, 247, 255)).\
            create_image(window_width, window_height)

        self.world_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)

        self.score_label = pyglet.text.Label(text="Score: 0",
                                             x=10,
                                             y=800,
                                             font_size=24,
                                             bold=True,
                                             color=(255, 255, 255, 255))
        self.lives_label = pyglet.text.Label(text="Lives: 0",
                                             x=200,
                                             y=800,
                                             font_size=24,
                                             bold=True,
                                             color=(255, 255, 255, 255))
        self.level_label = pyglet.text.Label(text="Level: 0",
                                             x=340,
                                             y=800,
                                             font_size=24,
                                             bold=True,
                                             color=(255, 255, 255, 255))

        self.fps_display = FPSDisplay(window)
        self.levels = [Level3(), Level1(), Level2()]
        self.on_new_level()

    def on_new_level(self):
        # Physics stuff
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.0, -1200.0)

        self.player = Rabbit(x=100,
                             y=600,
                             group=self.background,
                             space=self.space,
                             game=self)
        self.window.push_handlers(self.player.key_handler)
        self.current_level().create(self.space, self.background)

    def current_level(self):
        return self.levels[state['level']]

    def sticky_draw(self, obj, win):
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

    def update_labels(self):
        self.score_label.text = "Score: " + str(state['score'])
        self.lives_label.text = "Lives: " + str(state['lives'])
        self.level_label.text = "Level: " + str(state['level'])

    def update(self, dt):
        self.space.step(dt)
        self.player.update(dt)
        self.current_level().update(dt)
        self.update_labels()

    def draw(self):
        self.background_colour.blit(state['screen_pan_x'], 0)
        self.current_level().draw()
        self.player.draw()
        #draw_debug_box(rabbit)
        #draw_debug_box(carrot)
        #draw_debug_box(moving_platform)
        #draw_debug_box(p10)
        self.fps_display.draw()

        self.sticky_draw(self.score_label, self.window)
        self.sticky_draw(self.lives_label, self.window)
        self.sticky_draw(self.level_label, self.window)

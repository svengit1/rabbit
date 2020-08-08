import pyglet as pyglet
import pyglet.gl as gl
import pymunk
from pyglet.window import FPSDisplay
from pymunk import Vec2d
from pymunk.pyglet_util import DrawOptions

from level.level1 import Level1
from level.level2 import Level2
from player.player import Player
from resources import background_image, state, window_height, window_width


class Game:
    def __init__(self, window, debug=False):
        self.window = window
        self.background_colour = pyglet.image.SolidColorImagePattern((143, 187, 247, 255)).\
            create_image(window_width, window_height)

        self.world_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        label_y_position = window_height - 35
        self.score_label = pyglet.text.Label(text="Score: 0",
                                             x=10,
                                             y=label_y_position,
                                             font_size=24,
                                             bold=True,
                                             color=(255, 255, 255, 255))
        self.lives_label = pyglet.text.Label(text="Lives: 0",
                                             x=200,
                                             y=label_y_position,
                                             font_size=24,
                                             bold=True,
                                             color=(255, 255, 255, 255))
        self.level_label = pyglet.text.Label(text="Level: 0",
                                             x=340,
                                             y=label_y_position,
                                             font_size=24,
                                             bold=True,
                                             color=(255, 255, 255, 255))

        self.fps_display = FPSDisplay(window)
        self.levels = [Level1(self), Level2(self)]
        self.on_new_level()
        self.draw_options = DrawOptions()
        self.debug = debug

    def on_new_level(self):
        # Physics stuff
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.0, -1200.0)

        self.player = Player(x=100,
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
        dt = 1 / 60.
        for _ in range(10):
            self.space.step(dt/10)
        self.player.update(dt)
        self.current_level().update(dt)
        self.update_labels()

    def draw(self):
        self.window.clear()
        background_image.blit(state['screen_pan_x'], state['screen_pan_y'])
        #        self.background_colour.blit(state['screen_pan_x'], 0)
        if not self.debug:
            self.current_level().draw()
            self.player.draw()
        else:
            self.current_level().draw()
            self.player.draw()
            self.space.debug_draw(self.draw_options)
        #draw_debug_box(self.player.shape, self.player.body)
        self.fps_display.draw()

        self.sticky_draw(self.score_label, self.window)
        self.sticky_draw(self.lives_label, self.window)
        self.sticky_draw(self.level_label, self.window)

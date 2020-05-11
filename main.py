import pyglet as pyglet

from game import Game
from resources import window_height, window_width

window = pyglet.window.Window(window_width, window_height)

game = Game(window)


@window.event
def on_draw():
    window.clear()
    game.draw()


def update(dt):
    dt = 1.0 / 120.
    game.update(dt)


if __name__ == "__main__":
    # Start it up!
    # Update the 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()

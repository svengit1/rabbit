import getopt
import sys

import pyglet as pyglet
from pyglet.sprite import Sprite

from game import Game
from player.player_animation import PlayerAnimation
from resources import window_height, window_width


def main():
    # Start it up!
    short_options = "d"
    long_options = ["debug"]
    debug = False
    try:
        full_cmd_arguments = sys.argv

        # Keep all but the first
        argument_list = full_cmd_arguments[1:]

        arguments, values = getopt.getopt(argument_list, short_options,
                                          long_options)
        opts = [o for o, v in arguments]

        window = pyglet.window.Window(window_width, window_height)
        window.config.alpha_size = 8

        if '-d' in opts or '--debug' in opts:
            game = Game(window, True)
        else:
            game = Game(window)

        @window.event
        def on_draw():
            window.clear()
            game.draw()

        # Update the 120 times per second
        pyglet.clock.schedule_interval(game.update, 1 / 60.0)

        pyglet.app.run()

    except getopt.error as err:
        # Output error, and return with an error code
        print(str(err))
        sys.exit(2)


if __name__ == "__main__":
    main()

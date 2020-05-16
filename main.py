import pyglet as pyglet
from pyglet.sprite import Sprite

from game import Game
from player.player_animation import PlayerAnimation
from resources import window_height, window_width

window = pyglet.window.Window(window_width, window_height)

game = Game(window)
pa = PlayerAnimation()
t = [
    Sprite(img=pa.get_animation(PlayerAnimation.RUN_RIGHT), x=50, y=50),
    Sprite(img=pa.get_animation(PlayerAnimation.FLY_RIGHT), x=120, y=50),
    Sprite(img=pa.get_animation(PlayerAnimation.KICK_RIGHT), x=160, y=50),
    Sprite(img=pa.get_animation(PlayerAnimation.POWER_KICK_RIGHT), x=210,
           y=50),
    Sprite(img=pa.get_animation(PlayerAnimation.PUNCH_RIGHT), x=270, y=50),
    Sprite(img=pa.get_animation(PlayerAnimation.ROLL_RIGHT), x=330, y=50),
    Sprite(img=pa.get_animation(PlayerAnimation.STAND_RIGHT), x=380, y=50),
    Sprite(img=pa.get_animation(PlayerAnimation.JUMP_RIGHT), x=440, y=50),
    Sprite(img=pa.get_animation(PlayerAnimation.FALL_RIGHT), x=490, y=50),
    Sprite(img=pa.get_animation(PlayerAnimation.ROLL_LEFT), x=580, y=50),
]


@window.event
def on_draw():
    window.clear()
    game.draw()
    [i.draw() for i in t]


def update(dt):
    dt = 1.0 / 120.
    game.update(dt)


if __name__ == "__main__":
    # Start it up!
    # Update the 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()

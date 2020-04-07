import pyglet
import game.map_entity
from pyglet.window import key
import math
from game.resources import rabbit_images
import pymunk
from pymunk import Vec2d
from pymunk import Body


class Rabbit(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        self.space = kwargs['space']
        kwargs.pop('space')
        super().__init__(img=rabbit_images, **kwargs)
        self.key_handler = key.KeyStateHandler()
        self.velocity = 100
        rabbit_imgs_right = []
        rabbit_imgs_left = []

        for i in range(16, len(game.resources.rabbit_images) - 3, 3):
            image = pyglet.image.Texture.create(128, 96)
            for j in range(3):
                image.blit_into(rabbit_images[i + j].get_image_data(), 0, 32 * j, 0)
            image.anchor_x = 64
            rabbit_imgs_right.append(image)
            rabbit_imgs_left.append(image.get_transform(flip_x=True))
        self.jump_right = rabbit_imgs_right[1]
        self.fall_right = rabbit_imgs_right[0]
        self.jump_left = rabbit_imgs_left[1]
        self.fall_left = rabbit_imgs_left[0]
        self.rabbit_run_right = pyglet.image.Animation.from_image_sequence(rabbit_imgs_right[8:12], 0.08)
        self.rabbit_run_left = pyglet.image.Animation.from_image_sequence(rabbit_imgs_left[8:12], 0.08)
        self.rabbit_still_right = rabbit_imgs_right[7]
        self.rabbit_still_left = rabbit_imgs_left[7]
        self.image = self.rabbit_still_right

        vs = [(0, 10), (0, -10), (64, 10), (64, -10)]
        mass = 20
        moment = pymunk.moment_for_poly(mass, vs)
        self.body = pymunk.Body(mass, moment)
        self.shape = pymunk.Poly(self.body, vs)
        self.shape.friction = 0.5
        self.body.position = kwargs['x'], kwargs['y']
        self.body.angle = 0.5 * math.pi
        self.space.add(self.body, self.shape)
        self.body.center_of_gravity = 10, 0

    def update(self, dt):
        self.x = self.body.position.x
        self.y = self.body.position.y
        # print(self.body.velocity.y)
        # print(self.body.velocity.x)

        if self.key_handler[key.UP] and self.body.velocity.y == 0:
            self.body.apply_impulse_at_local_point([7850, 0], (0, 0))

        if self.body.velocity.x < 0 or self.image == self.rabbit_still_left or self.image == self.jump_left:
            if self.body.velocity.y < -8.0:
                self.image = self.fall_left
            if self.body.velocity.y > 10.0:
                self.image = self.jump_left

        if self.body.velocity.x > 2.5 or self.image == self.rabbit_still_right or self.image == self.jump_right:
            if self.body.velocity.y > 10.0:
                self.image = self.jump_right
            if self.body.velocity.y < -8.0:
                self.image = self.fall_right

        # left movement
        if self.key_handler[key.LEFT] and self.body.velocity.y == 0:
            if self.body.velocity.x >= 0:
                self.image = self.rabbit_run_left
            self.body.apply_impulse_at_local_point([0, 175], (0, 0))
        # right x movement
        if self.key_handler[key.RIGHT] and self.body.velocity.y == 0:
            if self.body.velocity.x <= 0:
                self.image = self.rabbit_run_right
            self.body.apply_impulse_at_local_point([0, -175], (0, 0))
        # standing
        if not self.key_handler[key.RIGHT] and not self.key_handler[key.LEFT] \
                and not self.key_handler[key.UP] and self.body.velocity.y == 0.0:
            if self.image == self.rabbit_run_right or self.image == self.fall_right:
                self.image = self.rabbit_still_right
            elif self.image == self.rabbit_run_left or self.image == self.fall_left:
                self.image = self.rabbit_still_left

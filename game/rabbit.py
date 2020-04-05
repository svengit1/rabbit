import pyglet
import game.map_entity
from pyglet.window import key
from game.resources import rabbit_images


class Rabbit(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(img=rabbit_images, **kwargs)
        self.velocity_x, self.velocity_y = 15.0, 0.0
        self.key_handler = key.KeyStateHandler()
        self.velocity = 450
        rabbit_imgs_right = []
        rabbit_imgs_left = []

        for i in range(16, len(game.resources.rabbit_images) - 3, 3):
            image = pyglet.image.Texture.create(128, 96)
            for j in range(3):
                image.blit_into(rabbit_images[i + j].get_image_data(), 0, 32 * j, 0)
            image.anchor_x = 64
            rabbit_imgs_right.append(image)
            rabbit_imgs_left.append(image.get_transform(flip_x=True))

        self.rabbit_run_right = pyglet.image.Animation.from_image_sequence(rabbit_imgs_right[8:12], 0.08)
        self.rabbit_run_left = pyglet.image.Animation.from_image_sequence(rabbit_imgs_left[8:12], 0.08)
        self.rabbit_still_right = rabbit_imgs_right[7]
        self.rabbit_still_left = rabbit_imgs_left[7]
        self.image = self.rabbit_run_right

    def update(self, dt):
        #super(Rabbit, self).update(dt)
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        if self.key_handler[key.LEFT]:
            if self.velocity_x >= 0:
                self.image = self.rabbit_run_left
                self.velocity_x = 0
            self.velocity_x = -self.velocity

        if self.key_handler[key.RIGHT]:
            if self.velocity_x <= 0:
                self.image = self.rabbit_run_right
                self.velocity_x = 0
            self.velocity_x = self.velocity

        if not self.key_handler[key.RIGHT] and not self.key_handler[key.LEFT]:
            if self.velocity_x > 0:
                self.image = self.rabbit_still_right
            elif self.velocity_x < 0:
                self.image = self.rabbit_still_left
            self.velocity_x = 0

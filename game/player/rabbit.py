import pyglet
import game.map_entity
from pyglet.window import key
import math
from game.resources import rabbit_images, state
import pymunk
from pyglet.gl import glTranslatef
from game.player._rabbit import PlayerFSM
from transitions import Machine, MachineError


class Rabbit(pyglet.sprite.Sprite, PlayerFSM):

    def __init__(self, *args, **kwargs):
        self.space = kwargs['space']
        kwargs.pop('space')
        super().__init__(img=rabbit_images, **kwargs)
        self.key_handler = key.KeyStateHandler()
        self.x, self.y =  kwargs['x'], kwargs['y']
        self.__init_state()
        self.__init_graphics()
        self.__init_physics()

    def __init_state(self):
        self.machine = Machine(self, states=Rabbit.states, initial='fr')
        self.fsm()
        self.standing_on_ground = False

    def __init_graphics(self):
        rabbit_imgs_left, rabbit_imgs_right = Rabbit.make_sprite_image()
        self.jump_right = rabbit_imgs_right[1]
        self.fall_right = rabbit_imgs_right[0]
        self.jump_left = rabbit_imgs_left[1]
        self.fall_left = rabbit_imgs_left[0]
        self.rabbit_run_right = pyglet.image.Animation.from_image_sequence(rabbit_imgs_right[8:12], 0.08)
        self.rabbit_run_right_beginning = rabbit_imgs_right[8]
        self.rabbit_run_left = pyglet.image.Animation.from_image_sequence(rabbit_imgs_left[8:12], 0.08)
        self.rabbit_still_right = rabbit_imgs_right[7]
        self.rabbit_still_left = rabbit_imgs_left[7]
        self.image = self.rabbit_still_right

    def __init_physics(self):
        self.running_velocity = 450
        self.velocity_comp = math.sqrt(self.running_velocity ** 2 / 2)
        vs = [(0, 10), (0, -10), (64, 10), (64, -10)]
        mass = 40
        moment = pymunk.moment_for_poly(mass, vs)
        self.body = pymunk.Body(mass, moment)
        self.shape = pymunk.Poly(self.body, vs)
        self.shape.friction = 1.0
        self.body.position = self.x, self.y
        self.body.angle = 0.5 * math.pi
        self.space.add(self.body, self.shape)
        self.body.center_of_gravity = 10, 0

    @staticmethod
    def make_sprite_image():
        rabbit_imgs_right = []
        rabbit_imgs_left = []
        for i in range(16, len(game.resources.rabbit_images) - 3, 3):
            image = pyglet.image.Texture.create(128, 96)
            for j in range(3):
                image.blit_into(rabbit_images[i + j].get_image_data(), 0, 32 * j, 0)
            image.anchor_x = 64
            rabbit_imgs_right.append(image)
            rabbit_imgs_left.append(image.get_transform(flip_x=True))
        return rabbit_imgs_left, rabbit_imgs_right

    def update(self, dt):
        self.__update_screen_pan(dt)
        self.x = self.body.position.x
        self.y = self.body.position.y
        self.__update_state(dt)
        self.__update_movement(dt)

    def __update_screen_pan(self, dt):
        # panning camera
        if 430 < self.x:
            state['screen_pan_x'] += -(self.x - self.body.position.x)
            glTranslatef((self.x - self.body.position.x), 0, 0)

        if self.y < 10:
            self.body.position = (100, 800)
            self.body.velocity = (0, 0)
            if self.x > 430:
                state['screen_pan_x'] += -(self.x - 430)
                glTranslatef(self.x - 430, 0, 0)

    def __update_state(self, dt):
        if len(self.space.shape_query(self.shape)) > 0:
            self.standing_on_ground = True
        else:
            self.standing_on_ground = False

        try:
            if math.isclose(self.body.velocity.x, 0, abs_tol=0.01) \
                    and math.isclose(self.body.velocity.y, 0, abs_tol=0.01):
                self.stop()
            elif self.body.velocity.y > 1 and not self.standing_on_ground:
                self.jump()
            elif self.body.velocity.y < -1 and not self.standing_on_ground:
                self.fall()
            elif self.body.velocity.x > 0:
                self.run_right()
            elif self.body.velocity.x < 0:
                self.run_left()
        except MachineError as msg:
            # State not allowed
            #print(msg)
            pass

    def __update_movement(self, dt):
        # jump
        if self.key_handler[key.UP] and self.standing_on_ground:
            self.body.apply_impulse_at_local_point([18550, 0], (0, 0))
            self.standing_on_ground = False

        # left movement
        if not self.key_handler[key.RIGHT] and self.key_handler[key.LEFT] and self.standing_on_ground:
            if self.body.velocity.y > 1:
                speed_x, speed_y = -self.velocity_comp - 50, self.velocity_comp
            else:
                speed_x, speed_y = -self.running_velocity, self.body.velocity.y
            self.body.velocity = (speed_x, speed_y)

        # slow down in jump
        if not self.standing_on_ground:
            if self.body.velocity.x > 0 and self.key_handler[key.LEFT]:
                self.body.apply_impulse_at_local_point([0, 100], (0, 0))
            if self.body.velocity.x < 0 and self.key_handler[key.RIGHT]:
                self.body.apply_impulse_at_local_point([0, -100], (0, 0))
  
        # right movement
        if not self.key_handler[key.LEFT] and self.key_handler[key.RIGHT] and self.standing_on_ground:
            if self.body.velocity.y > 1:
                speed_x, speed_y = self.velocity_comp + 50, self.velocity_comp
            else:
                speed_x, speed_y = self.running_velocity, self.body.velocity.y
            self.body.velocity = (speed_x, speed_y)

        if self.standing_on_ground and not self.key_handler[key.UP] and \
           not self.key_handler[key.RIGHT] and not self.key_handler[key.LEFT]:
            self.body.velocity = (0, 0)

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
        self.touching_ground = False
        self.still = False

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
        self.speed_limit_y = 200
        self.jump_force = 20000
        self.running_velocity = 450
        self.velocity_comp = math.sqrt(self.running_velocity ** 2 / 2)
        vs = [(0, 10), (0, -10), (64, 10), (64, -10)]
        mass = 40
        moment = pymunk.moment_for_poly(mass, vs)
        self.body = pymunk.Body(mass, moment)
        self.shape = pymunk.Poly(self.body, vs)
        self.shape.friction = 1.0
        self.shape.collision_type = 1
        self.body.position = self.x, self.y
        self.body.angle = 0.5 * math.pi
        self.space.add(self.body, self.shape)
        self.body.center_of_gravity = 10, 0
        self.carrot_collision_handler = self.space.add_collision_handler(1, 2)
        self.carrot_collision_handler.pre_solve = self.collision_with_food
        self.platform_collision_handler = self.space.add_collision_handler(1, 3)
        self.platform_collision_handler.pre_solve = self.standing_on_platform

    def collision_with_food(self, arbiter, space, data):
        state['score'] += arbiter.shapes[1].sprite.points
        space.remove(arbiter.shapes[1])
        arbiter.shapes[1].sprite.batch = None
        return False

    def standing_on_platform(self, arbiter, space, data):
        self.still = arbiter.shapes[0].body.velocity == arbiter.shapes[1].body.velocity
        return True


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
            self.touching_ground = True
        else:
            self.touching_ground = False
        try:
            if self.touching_ground and self.still:
                self.stop()
            elif self.body.velocity.y > 1 and not self.touching_ground:
                self.jump()
            elif self.body.velocity.y < -1 and not self.touching_ground:
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
        if self.key_handler[key.UP] and self.touching_ground and self.state not in ['jr', 'jl', 'fl', 'fr']\
                and self.body.velocity.y < self.speed_limit_y:
            self.body.apply_impulse_at_local_point([self.jump_force, 0], (0, 0))
            self.touching_ground = False

        # left movement
        if not self.key_handler[key.RIGHT] and self.key_handler[key.LEFT] and self.touching_ground:
            if self.body.velocity.y > 1:
                speed_x, speed_y = -self.velocity_comp - 50, self.velocity_comp
            else:
                speed_x, speed_y = -self.running_velocity, self.body.velocity.y
            self.body.velocity = (speed_x, speed_y)

        # slow down in jump
        if not self.touching_ground:
            if self.body.velocity.x > 0 and self.key_handler[key.LEFT]:
                self.body.apply_impulse_at_local_point([0, 150], (0, 0))
            if self.body.velocity.x < 0 and self.key_handler[key.RIGHT]:
                self.body.apply_impulse_at_local_point([0, -150], (0, 0))
  
        # right movement
        if not self.key_handler[key.LEFT] and self.key_handler[key.RIGHT] and self.touching_ground:
            if self.body.velocity.y > 1:
                speed_x, speed_y = self.velocity_comp + 50, self.velocity_comp
            else:
                speed_x, speed_y = self.running_velocity, self.body.velocity.y
            self.body.velocity = (speed_x, speed_y)
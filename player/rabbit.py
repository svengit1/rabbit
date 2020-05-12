import math

import pyglet
import pymunk
from pyglet.gl import glTranslatef
from pyglet.window import key
from transitions import Machine, MachineError

from player._rabbit import PlayerFSM
from resources import last_level, rabbit_images, state


class Rabbit(pyglet.sprite.Sprite, PlayerFSM):
    def __init__(self, *args, **kwargs):
        self.space = kwargs['space']
        self.game = kwargs['game']
        kwargs.pop('space')
        kwargs.pop('game')
        super().__init__(img=rabbit_images, **kwargs)
        self.key_handler = key.KeyStateHandler()
        self.x, self.y = kwargs['x'], kwargs['y']
        self.__init_state()
        self.__init_graphics()
        self.__init_physics()

    def __init_state(self):
        self.machine = Machine(self, states=Rabbit.states, initial='fr')
        self.fsm()
        self.touching_ground = False
        self.still = False
        self.on_slope = False

    def __init_graphics(self):
        rabbit_imgs_left, rabbit_imgs_right = Rabbit.make_sprite_image()
        self.jump_right = rabbit_imgs_right[1]
        self.fall_right = rabbit_imgs_right[0]
        self.jump_left = rabbit_imgs_left[1]
        self.fall_left = rabbit_imgs_left[0]
        self.rabbit_run_right = pyglet.image.Animation.from_image_sequence(
            rabbit_imgs_right[8:12], 0.08)
        self.rabbit_run_right_beginning = rabbit_imgs_right[8]
        self.rabbit_run_left = pyglet.image.Animation.from_image_sequence(
            rabbit_imgs_left[8:12], 0.08)
        self.rabbit_still_right = rabbit_imgs_right[7]
        self.rabbit_still_left = rabbit_imgs_left[7]
        self.image = self.rabbit_still_right

    def __init_physics(self):
        self.speed_limit_y = 200
        self.jump_force = 20000
        self.running_velocity = 450
        self.velocity_comp = math.sqrt(self.running_velocity**2 / 2)
        vs = [(0, 10), (0, -10), (64, 10), (64, -10)]
        mass = 40
        moment = pymunk.moment_for_poly(mass, vs)
        self.body = pymunk.Body(mass, moment)
        self.shape = pymunk.Poly(self.body, vs)
        self.shape.friction = 1.0
        self.shape.collision_type = 1
        self.shape.elasticity = 0.9
        self.body.position = self.x, self.y
        self.body.angle = 0.5 * math.pi
        self.space.add(self.body, self.shape)
        self.body.center_of_gravity = 10, 0
        # Collison handlers
        self.space.add_collision_handler(
            1, 2).pre_solve = self.collision_with_food
        self.platform_collision_handler = self.space.add_collision_handler(
            1, 3)
        self.slope_collision_handler = self.space.add_collision_handler(1, 4)
        self.level_end_collision_handler = self.space.add_collision_handler(
            1, 10)
        self.level_end_collision_handler.pre_solve = self.level_completed
        self.platform_collision_handler.pre_solve = self.standing_on_platform
        self.platform_collision_handler.separate = self.separated_from_platform
        self.slope_collision_handler.pre_solve = self.standing_on_slope
        self.slope_collision_handler.separate = self.separated_from_slope

    def level_completed(self, aarbiter, space, data):
        if state['level'] != last_level:
            state['level'] = state['level'] + 1
            self.game.on_new_level()
            self.pan_screen_to_origin()
        return False

    def collision_with_food(self, arbiter, space, data):
        state['score'] += arbiter.shapes[1].sprite.points
        space.remove(arbiter.shapes[1])
        self.game.current_level().scenery.remove(arbiter.shapes[1].sprite)
        return False

    def separated_from_slope(self, arbiter, space, data):
        self.on_slope = False

    @staticmethod
    def compare_velocity(vel_a, vel_b):
        return math.isclose(vel_a.x, vel_b.x, abs_tol=0.1) and math.isclose(
            vel_a.y, vel_b.y, abs_tol=0.1)

    def standing_on_slope(self, arbiter, space, data):
        self.still = self.compare_velocity(arbiter.shapes[0].body.velocity,
                                           arbiter.shapes[1].body.velocity)
        self.on_slope = True
        return True

    def separated_from_platform(self, arbiter, space, data):
        self.touching_ground = False

    def standing_on_platform(self, arbiter, space, data):
        self.still = self.compare_velocity(arbiter.shapes[0].body.velocity,
                                           arbiter.shapes[1].body.velocity)
        self.touching_ground = True
        return True

    @staticmethod
    def make_sprite_image():
        rabbit_imgs_right = []
        rabbit_imgs_left = []
        for i in range(16, len(rabbit_images) - 3, 3):
            image = pyglet.image.Texture.create(128, 96)
            for j in range(3):
                image.blit_into(rabbit_images[i + j].get_image_data(), 0,
                                32 * j, 0)
            image.anchor_x = 64
            rabbit_imgs_right.append(image)
            rabbit_imgs_left.append(image.get_transform(flip_x=True))
        return rabbit_imgs_left, rabbit_imgs_right

    def pan_screen_to_origin(self):
        if self.x > 430:
            state['screen_pan_x'] += -(self.x - 430)
            glTranslatef(self.x - 430, 0, 0)

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

        #Died
        if self.y < 10:
            self.body.position = (100, 800)
            self.body.velocity = (0, 0)
            state['lives'] = state['lives'] - 1
            if state['lives'] == 0:
                state['lives'] = 3
                state['score'] = 0
            self.pan_screen_to_origin()

    def __update_state(self, dt):
        try:
            if (self.touching_ground or self.on_slope) and self.still:
                self.stop()
            elif self.body.velocity.y > 1 and not self.touching_ground and not self.on_slope:
                self.jump()
            elif self.body.velocity.y < -1 and not self.touching_ground and not self.on_slope:
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
        if self.key_handler[key.UP] and (self.touching_ground or self.on_slope) and self.state not in ['jr', 'jl', 'fl', 'fr']\
                and self.body.velocity.y < self.speed_limit_y:
            self.body.apply_impulse_at_local_point([self.jump_force, 0],
                                                   (0, 0))
            self.touching_ground = False

        # left movement
        if not self.key_handler[key.RIGHT] and self.key_handler[key.LEFT] and (
                self.touching_ground or self.on_slope):
            speed_x, speed_y = -self.running_velocity, self.body.velocity.y
            self.body.velocity = (speed_x, speed_y)

        # slow down in jump
        if not self.touching_ground and not self.on_slope:
            if self.body.velocity.x > 0 and self.key_handler[key.LEFT]:
                self.body.apply_impulse_at_local_point([0, 150], (0, 0))
            if self.body.velocity.x < 0 and self.key_handler[key.RIGHT]:
                self.body.apply_impulse_at_local_point([0, -150], (0, 0))

        # right movement
        if not self.key_handler[key.LEFT] and self.key_handler[key.RIGHT] and (
                self.touching_ground or self.on_slope):
            speed_x, speed_y = self.running_velocity, self.body.velocity.y
            self.body.velocity = (speed_x, speed_y)

import math

import pyglet
import pymunk
from util.util import sign
from pyglet.gl import glTranslatef
from pyglet.window import key
from pymunk import Vec2d
from transitions import Machine, MachineError

from player.player_animation import PlayerAnimation
from player.player_fsm import PlayerFSM
from resources import last_level, rabbit_images, state


class Player(pyglet.sprite.Sprite, PlayerFSM):
    running_velocity = 500

    def __init__(self, *args, **kwargs):
        self.space = kwargs['space']
        self.game = kwargs['game']
        kwargs.pop('space')
        kwargs.pop('game')
        super().__init__(img=rabbit_images, **kwargs)
        self.key_handler = key.KeyStateHandler()
        self.x, self.y = kwargs['x'], kwargs['y']
        self.__init_state__()
        self.__init_graphics__()
        self.__init_physics__()

    def __init_state__(self):
        self.machine = Machine(self, states=Player.states, initial='fr')
        self.fsm()
        self.static_action = [
            'pr', 'pl', 'pkl', 'pkr', 'kl', 'kr', 'rrr', 'rrl'
        ]
        self.elapsed_since_last_action = 0

    def __init_graphics__(self):
        self.pa = PlayerAnimation()
        self.image = self.pa.get_animation(PlayerAnimation.STAND_RIGHT)

    def __init_physics__(self):
        self.jump_force = 25000
        self.moving_force = 2000000

        vs = [(-15, 0), (-15, 64), (15, 64), (15, 0)]
        mass = 40
        self.body = pymunk.Body(mass, pymunk.inf)
        self.shape = pymunk.Poly(self.body, vs)
        self.shape.friction = 0.5
        self.shape.collision_type = 1
        self.shape.elasticity = 0
        self.body.position = self.x, self.y
        self.body.touching_ground = False
        self.body.still = False
        self.space.add(self.body, self.shape)
        self.body.center_of_gravity = 0, 0
        self.body.velocity_func = self.limit_velocity
        self.body.current_max_velocity = self.running_velocity
        # Collison handlers
        self.space.add_collision_handler(
            1, 2).pre_solve = self.collision_with_food
        self.platform_collision_handler = self.space.add_collision_handler(
            1, 3)
        self.level_end_collision_handler = self.space.add_collision_handler(
            1, 10)
        self.spring_collision_handler = self.space.add_collision_handler(1, 5)
        self.level_end_collision_handler.pre_solve = self.level_completed
        self.platform_collision_handler.pre_solve = Player.standing_on_platform
        self.platform_collision_handler.separate = Player.separated_from_platform

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

    @staticmethod
    def limit_velocity(body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        l = body.velocity.x
        if abs(body.velocity.x) > abs(body.current_max_velocity):
            body.velocity = (body.current_max_velocity, body.velocity.y)

    @staticmethod
    def compare_velocity(vel_a, vel_b):
        return math.isclose(vel_a.x, vel_b.x, abs_tol=0.1) and math.isclose(
            vel_a.y, vel_b.y, abs_tol=0.1)

    @staticmethod
    def separated_from_platform(arbiter, space, data):
        arbiter.shapes[0].body.touching_ground = None

    @staticmethod
    def standing_on_platform(arbiter, space, data):
        normal = Vec2d(0, -1)
        if Player.compare_velocity(arbiter.contact_point_set.normal, normal):
            player_body = arbiter.shapes[0].body
            player_body.still = Player.compare_velocity(
                arbiter.shapes[0].body.velocity,
                arbiter.shapes[1].body.velocity)
            player_body.current_max_velocity = arbiter.shapes[
            1].body.velocity.x + sign(
                player_body.velocity.x) * Player.running_velocity
            player_body.touching_ground = arbiter.shapes[1].body
        return True

    def pan_screen_to_origin(self):
        if self.x > 430:
            state['screen_pan_x'] += -(self.x - 430)
            glTranslatef(self.x - 430, 0, 0)

        if 430 > self.y:
            state['screen_pan_y'] += -(self.y - 430)
            glTranslatef(0, (self.y - 430), 0)


    def update(self, dt):
        self.__update_screen_pan(dt)
        self.x = self.body.position.x
        self.y = self.body.position.y
        self.__update_state__(dt)
        self.__update_movement__(dt)
        self.animation_timer_reset(dt)

    def animation_timer_reset(self, dt):
        self.elapsed_since_last_action += dt
        if self.elapsed_since_last_action > 0.6:
            self.elapsed_since_last_action = 0
            if self.state in self.static_action:
                self.stop()

    def __update_screen_pan(self, dt):
        # panning camera
        if 430 < self.x:
            state['screen_pan_x'] += -(self.x - self.body.position.x)
            glTranslatef((self.x - self.body.position.x), 0, 0)

        if 430 < self.y:
            state['screen_pan_y'] += -(self.y - self.body.position.y)
            glTranslatef(0, (self.y - self.body.position.y), 0)

        #Died
        if self.y < 10:
            self.body.position = (100, 800)
            self.body.velocity = (0, 0)
            state['lives'] = state['lives'] - 1
            if state['lives'] == 0:
                state['lives'] = 3
                state['score'] = 0
            self.pan_screen_to_origin()

    def __update_state__(self, dt):
        try:
            if self.body.touching_ground and self.body.still and self.state not in self.static_action:
                self.stop()
            elif self.body.velocity.y > 1 and not self.body.touching_ground:
                self.jump()
            elif self.body.velocity.y < -1 and not self.body.touching_ground:
                self.fall()
            elif self.body.velocity.x > 0 and self.key_handler[
                    key.RIGHT] and not self.body.still and self.state != 'rr':
                self.run_right()
            elif self.body.velocity.x < 0 and self.key_handler[
                    key.LEFT] and not self.body.still and self.state != 'rl':
                self.run_left()
        except MachineError as msg:
            # State not allowed
            #print(msg)
            pass

    def __update_movement__(self, dt):
        # punch
        if self.key_handler[
                key.Q] and self.body.touching_ground and self.state in [
                    'sl', 'sr', 'rl', 'rr', 'pr', 'pl', 'pkr', 'pkl', 'kr',
                    'kl'
                ]:
            self.punch()
            self.elapsed_since_last_action = 0

        # power kick
        if self.key_handler[
                key.E] and self.body.touching_ground and self.state in [
                    'sl', 'sr', 'rl', 'rr', 'pr', 'pl', 'pkr', 'pkl', 'kr',
                    'kl'
                ]:
            self.pow_kick()
            self.elapsed_since_last_action = 0

        # kick
        if self.key_handler[
                key.W] and self.body.touching_ground and self.state in [
                    'sl', 'sr', 'rl', 'rr', 'pr', 'pl', 'pkr', 'pkl', 'kr',
                    'kl'
                ]:
            self.kick()
            self.elapsed_since_last_action = 0

        # jump
        if self.key_handler[
                key.UP] and self.body.touching_ground and self.state not in [
                    'jr', 'jl', 'fl', 'fr'
                ]:
            self.body.apply_impulse_at_local_point([0, self.jump_force],
                                                   (0, 15))
            self.body.touching_ground = False

        # roll
        if self.key_handler[key.DOWN] and self.body.touching_ground:
            if self.state in ['sr', 'sl', 'rl', 'rr']:
                if self.key_handler[key.RIGHT]:
                    self.run_right()
                    self.roll()
                    self.elapsed_since_last_action = 0
                elif self.key_handler[key.LEFT]:
                    self.run_left()
                    self.roll()
                    self.elapsed_since_last_action = 0

        # left movement
        if not self.key_handler[key.RIGHT] and self.key_handler[
                key.LEFT] and self.body.touching_ground or self.state == 'rrl':
            self.body.apply_force_at_local_point((-self.moving_force, 0), (0, 0))

        if not self.body.touching_ground:
            # slow down in jump
            if self.body.velocity.x > 0 and self.key_handler[key.LEFT]:
                self.body.apply_impulse_at_local_point([-350, 0], (0, 0))
            if self.body.velocity.x < 0 and self.key_handler[key.RIGHT]:
                self.body.apply_impulse_at_local_point([350, 0], (0, 0))
            # accelerate in jump
            if self.body.velocity.x <= 0 and self.key_handler[key.LEFT]:
                self.body.apply_impulse_at_local_point([-250, 0], (0, 0))
            if self.body.velocity.x >= 0 and self.key_handler[key.RIGHT]:
                self.body.apply_impulse_at_local_point([250, 0], (0, 0))

        # right movement
        if not self.key_handler[key.LEFT] and self.key_handler[
                key.
                RIGHT] and self.body.touching_ground or self.state == 'rrr':
            self.body.apply_force_at_local_point((self.moving_force, 0), (0, 0))


import math

import pymunk
from pyglet.sprite import Sprite
from pymunk import Vec2d
from transitions import Machine, MachineError

from enemy.enemy_animation import EnemyAnimation
from enemy.enemy_fsm import EnemyFSM
from map_objects.moving_platform import MovingPlatform
from map_objects.platform import Platform
from resources import segment_height, segment_width


class Enemy(Sprite, EnemyFSM):
    max_relative_velocity = 100

    def __init__(self, space, **kwargs):
        self.initial_positition = kwargs['initial_position']
        self.level = kwargs['level']
        kwargs.pop('initial_position')
        kwargs.pop('level')
        self.ea = EnemyAnimation.instance(20)
        super(Enemy, self).__init__(img=self.ea.get_animation(
            EnemyAnimation.WALK_RIGHT, duration=0.1, loop=True),
                                    **kwargs)
        self.space = space
        self.machine = Machine(self, states=Enemy.states, initial='wr')
        self.fsm()

        self.__init_physiscs__()

    def __init_physiscs__(self):
        image_width = self.image.get_max_width() * 0.8
        offset = self.image.get_max_width() - image_width
        vs = [(offset, 0), (image_width, 0), (image_width, 64), (offset, 64)]
        mass = 30
        moment = pymunk.moment_for_poly(mass, vs)
        self.body = pymunk.Body(mass, moment)
        self.shape = pymunk.Poly(self.body, vs)
        self.shape.friction = 0
        self.shape.collision_type = 20
        self.shape.elasticity = 0
        self.body.position = (segment_width * self.initial_positition[0],  self.initial_positition[0] * segment_height)
        self.body.center_of_gravity = 20, 0
        self.body.velocity_func = self.limit_velocity
        self.body.min_walk_x, self.body.max_walk_x = 0, 0
        self.body.current_max_velocity = Enemy.max_relative_velocity
        self.body.touching_ground = False
        self.moving_force = (40000, 0)
        self.space.add(self.body, self.shape)
        # Collison handlers
        self.platform_collision_handler = self.space.add_collision_handler(
            20, 3)
        self.player_collision_handler = self.space.add_collision_handler(20, 1)
        self.player_collision_handler.pre_solve = Enemy.attack
        self.player_collision_handler.separate = Enemy.cease_attack
        self.platform_collision_handler.pre_solve = Enemy.standing_on_platform
        self.platform_collision_handler.separate = Enemy.separated_from_platform
        self.body.attack = False

    @staticmethod
    def compare_velocity(vel_a, vel_b):
        return math.isclose(vel_a.x, vel_b.x, abs_tol=0.1) and math.isclose(
            vel_a.y, vel_b.y, abs_tol=0.1)

    @staticmethod
    def separated_from_platform(arbiter, space, data):
        arbiter.shapes[0].body.touching_ground = None

    @staticmethod
    def attack(arbiter, space, data):
        arbiter.shapes[0].body.attack = True
        return True

    @staticmethod
    def cease_attack(arbiter, space, data):
        arbiter.shapes[0].body.attack = False
        return True

    @staticmethod
    def sign(x):
        if x >= 0:
            return 1
        return -1

    @staticmethod
    def standing_on_platform(arbiter, space, data):
        enemy_body = arbiter.shapes[0].body
        position_x = arbiter.shapes[1].body.position.x
        enemy_body.max_walk_x = max(arbiter.shapes[1].get_vertices(),
                                    key=lambda k: k.x).x + position_x
        enemy_body.min_walk_x = min(arbiter.shapes[1].get_vertices(),
                                    key=lambda k: k.x).x + position_x
        enemy_body.current_max_velocity = arbiter.shapes[
            1].body.velocity.x + Enemy.sign(
                enemy_body.velocity.x) * Enemy.max_relative_velocity
        enemy_body.touching_ground = arbiter.shapes[1].body
        return True

    @staticmethod
    def guards(platform, g, level):
        assert isinstance(platform, Platform) or isinstance(
            platform, MovingPlatform)
        e = Enemy(platform.space,
                  initial_position=(platform.hpos, platform.vpos),
                  group=g,
                  level=level)
        return e

    @staticmethod
    def limit_velocity(body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        l = body.velocity.x
        if abs(body.velocity.x) > abs(body.current_max_velocity):
            body.velocity = (body.current_max_velocity, body.velocity.y)

    def __update_state__(self, dt):
        try:
            if self.body.touching_ground and self.body.still and self.state not in self.static_action:
                self.stop()
            elif self.body.velocity.x > 0:
                self.walk_right()
            elif self.body.velocity.x < 0:
                self.walk_left()
        except MachineError as msg:
            # State not allowed
            #print(msg)
            pass

    def update(self, dt):
        self.x = self.body.position.x
        self.y = self.body.position.y

        if math.isclose(
                self.x, self.body.max_walk_x, abs_tol=self.image.get_max_width(
                )) and self.body.velocity.x > 0:

            self.body.velocity = (self.body.velocity.x * -1,
                                  self.body.velocity.y)

            self.moving_force = tuple([i * -1 for i in self.moving_force])
            if self.body.attack:
                self.image = self.ea.get_animation(EnemyAnimation.ATTACK_LEFT,
                                                   duration=0.1,
                                                   loop=True)
            else:
                self.image = self.ea.get_animation(EnemyAnimation.WALK_LEFT,
                                                   duration=0.1,
                                                   loop=True)

        if math.isclose(self.x, self.body.min_walk_x,
                        abs_tol=10) and self.body.velocity.x < 0:
            self.body.velocity = (self.body.velocity.x * -1,
                                  self.body.velocity.y)
            self.moving_force = tuple([i * -1 for i in self.moving_force])
            if self.body.attack:
                self.image = self.ea.get_animation(EnemyAnimation.ATTACK_RIGHT,
                                                   duration=0.1,
                                                   loop=True)
            else:
                self.image = self.ea.get_animation(EnemyAnimation.WALK_RIGHT,
                                                   duration=0.1,
                                                   loop=True)
        if self.body.touching_ground:
            self.body.apply_force_at_local_point(self.moving_force, (20, 0))

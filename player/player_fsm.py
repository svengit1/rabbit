from transitions import Machine, MachineError

from player.player_animation import PlayerAnimation


class PlayerFSM():
    states = [
        'rl', 'rr', 'sl', 'sr', 'jl', 'jr', 'fl', 'fr', 'pr', 'pl', 'kl', 'kr',
        'pkl', 'pkr', 'rrr', 'rrl'
    ]

    def fsm(self):
        self.machine.add_transition('run_left', 'sl', 'rl')
        self.machine.add_transition('run_left', 'sr', 'rl')
        self.machine.add_transition('run_left', 'fl', 'rl')
        self.machine.add_transition('run_left', 'fr', 'rl')
        self.machine.add_transition('run_left', 'rr', 'rl')
        self.machine.add_transition('run_right', 'sl', 'rr')
        self.machine.add_transition('run_right', 'sr', 'rr')
        self.machine.add_transition('run_right', 'fr', 'rr')
        self.machine.add_transition('run_right', 'fl', 'rr')
        self.machine.add_transition('run_right', 'rl', 'rr')

        self.machine.add_transition('jump', 'sl', 'jl')
        self.machine.add_transition('jump', 'sr', 'jr')
        self.machine.add_transition('fall', 'jl', 'fl')
        self.machine.add_transition('fall', 'jr', 'fr')
        self.machine.add_transition('fall', 'rl', 'fl')
        self.machine.add_transition('fall', 'rr', 'fr')
        self.machine.add_transition('fall', 'sl', 'fl')
        self.machine.add_transition('fall', 'sr', 'fr')
        self.machine.add_transition('jump', 'rl', 'jl')
        self.machine.add_transition('jump', 'rr', 'jr')
        self.machine.add_transition('stop', 'rr', 'sr')
        self.machine.add_transition('stop', 'rl', 'sl')
        self.machine.add_transition('stop', 'jr', 'fr')
        self.machine.add_transition('stop', 'jl', 'fl')
        self.machine.add_transition('stop', 'fr', 'sr')
        self.machine.add_transition('stop', 'fl', 'sl')
        self.machine.add_transition('stop', 'rrr', 'sr')
        self.machine.add_transition('stop', 'rrl', 'sl')

        self.machine.add_transition('punch', 'sl', 'pl')
        self.machine.add_transition('punch', 'sr', 'pr')
        self.machine.add_transition('punch', 'pl', 'pl')
        self.machine.add_transition('punch', 'pr', 'pr')
        self.machine.add_transition('punch', 'rr', 'pr')
        self.machine.add_transition('punch', 'rl', 'pl')

        self.machine.add_transition('punch', 'pkl', 'pl')
        self.machine.add_transition('punch', 'pkr', 'pr')
        self.machine.add_transition('punch', 'kr', 'pr')
        self.machine.add_transition('punch', 'kl', 'pl')

        self.machine.add_transition('stop', 'pl', 'sl')
        self.machine.add_transition('stop', 'pr', 'sr')
        self.machine.add_transition('run_right', 'pr', 'rr')
        self.machine.add_transition('run_right', 'rr', 'rr')
        self.machine.add_transition('run_left', 'pl', 'rl')
        self.machine.add_transition('run_right', 'pl', 'rr')
        self.machine.add_transition('run_left', 'pr', 'rl')
        self.machine.add_transition('run_left', 'rl', 'rl')

        self.machine.add_transition('jump', 'pl', 'jl')
        self.machine.add_transition('jump', 'pr', 'jr')

        self.machine.add_transition('kick', 'sl', 'kl')
        self.machine.add_transition('kick', 'sr', 'kr')
        self.machine.add_transition('kick', 'kl', 'kl')
        self.machine.add_transition('kick', 'kr', 'kr')
        self.machine.add_transition('kick', 'rr', 'kr')
        self.machine.add_transition('kick', 'rl', 'kl')

        self.machine.add_transition('kick', 'pkr', 'kr')
        self.machine.add_transition('kick', 'pkl', 'kl')
        self.machine.add_transition('kick', 'pr', 'kr')
        self.machine.add_transition('kick', 'pl', 'kl')

        self.machine.add_transition('stop', 'kl', 'sl')
        self.machine.add_transition('stop', 'kr', 'sr')
        self.machine.add_transition('run_right', 'kr', 'rr')
        self.machine.add_transition('run_left', 'kl', 'rl')
        self.machine.add_transition('run_right', 'kl', 'rr')
        self.machine.add_transition('run_left', 'kr', 'rl')
        self.machine.add_transition('jump', 'kl', 'jl')
        self.machine.add_transition('jump', 'kr', 'jr')

        self.machine.add_transition('pow_kick', 'sl', 'pkl')
        self.machine.add_transition('pow_kick', 'sr', 'pkr')
        self.machine.add_transition('pow_kick', 'pkl', 'pkl')
        self.machine.add_transition('pow_kick', 'pkr', 'pkr')
        self.machine.add_transition('pow_kick', 'rr', 'pkr')
        self.machine.add_transition('pow_kick', 'rl', 'pkl')
        self.machine.add_transition('pow_kick', 'pl', 'pkl')
        self.machine.add_transition('pow_kick', 'pr', 'pkr')
        self.machine.add_transition('pow_kick', 'kr', 'pkr')
        self.machine.add_transition('pow_kick', 'kl', 'pkl')

        self.machine.add_transition('stop', 'pkl', 'sl')
        self.machine.add_transition('stop', 'pkr', 'sr')
        self.machine.add_transition('run_right', 'pkr', 'rr')
        self.machine.add_transition('run_left', 'pkl', 'rl')
        self.machine.add_transition('run_right', 'pkl', 'rr')
        self.machine.add_transition('run_left', 'pkr', 'rl')
        self.machine.add_transition('jump', 'pkl', 'jl')
        self.machine.add_transition('jump', 'pkr', 'jr')

        self.machine.add_transition('jump', 'fl', 'jl')
        self.machine.add_transition('jump', 'fr', 'jr')

        self.machine.add_transition('roll', 'sl', 'rrl')
        self.machine.add_transition('roll', 'sr', 'rrr')
        self.machine.add_transition('roll', 'rl', 'rrl')
        self.machine.add_transition('roll', 'rr', 'rrr')

    def on_enter_rr(self):
        self.image = self.pa.get_animation(PlayerAnimation.RUN_RIGHT,
                                           duration=0.08,
                                           loop=True)

    def on_enter_rl(self):
        self.image = self.pa.get_animation(PlayerAnimation.RUN_LEFT,
                                           duration=0.08,
                                           loop=True)

    def on_enter_sr(self):
        self.image = self.pa.get_animation(PlayerAnimation.STAND_RIGHT,
                                           duration=0.3,
                                           loop=True)

    def on_enter_sl(self):
        self.image = self.pa.get_animation(PlayerAnimation.STAND_LEFT,
                                           duration=0.3,
                                           loop=True)

    def on_enter_fl(self):
        self.image = self.pa.get_animation(PlayerAnimation.FALL_LEFT)

    def on_enter_fr(self):
        self.image = self.pa.get_animation(PlayerAnimation.FALL_RIGHT)

    def on_enter_jl(self):
        self.image = self.pa.get_animation(PlayerAnimation.JUMP_LEFT,
                                           duration=0.1,
                                           loop=False)

    def on_enter_jr(self):
        self.image = self.pa.get_animation(PlayerAnimation.JUMP_RIGHT,
                                           duration=0.1,
                                           loop=False)

    def on_enter_pr(self):
        self.image = self.pa.get_animation(PlayerAnimation.PUNCH_RIGHT,
                                           duration=0.1,
                                           loop=False)

    def on_enter_pl(self):
        self.image = self.pa.get_animation(PlayerAnimation.PUNCH_LEFT,
                                           duration=0.1,
                                           loop=False)

    def on_enter_kl(self):
        self.image = self.pa.get_animation(PlayerAnimation.KICK_LEFT,
                                           duration=0.1,
                                           loop=False)

    def on_enter_kr(self):
        self.image = self.pa.get_animation(PlayerAnimation.KICK_RIGHT,
                                           duration=0.1,
                                           loop=False)

    def on_enter_pkl(self):
        self.image = self.pa.get_animation(PlayerAnimation.POWER_KICK_LEFT,
                                           duration=0.05,
                                           loop=False)

    def on_enter_pkr(self):
        self.image = self.pa.get_animation(PlayerAnimation.POWER_KICK_RIGHT,
                                           duration=0.05,
                                           loop=False)

    def on_enter_rrr(self):
        self.image = self.pa.get_animation(PlayerAnimation.ROLL_RIGHT,
                                           duration=0.1,
                                           loop=False)

    def on_enter_rrl(self):
        self.image = self.pa.get_animation(PlayerAnimation.ROLL_LEFT,
                                           duration=0.1,
                                           loop=False)

from transitions import Machine, MachineError

from player.player_animation import PlayerAnimation


class PlayerFSM():
    states = ['rl', 'rr', 'sl', 'sr', 'jl', 'jr', 'fl', 'fr']

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
        self.machine.add_transition('touched_ground', 'fr', 'sr')
        self.machine.add_transition('touched_ground', 'fl', 'sl')
        self.machine.add_transition('stop', 'jr', 'fr')
        self.machine.add_transition('stop', 'jl', 'fl')
        self.machine.add_transition('stop', 'fr', 'sr')
        self.machine.add_transition('stop', 'fl', 'sl')
        self.machine.add_transition('punch', 'sl', 'pl')
        self.machine.add_transition('punch', 'sr', 'pr')

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
        self.image = self.pa.get_animation(PlayerAnimation.PUNCH_RIGHT,
                                           duration=0.1,
                                           loop=False)

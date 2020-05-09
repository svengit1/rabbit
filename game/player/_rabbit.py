from transitions import Machine, MachineError


class PlayerFSM():
    states = ['rl', 'rr', 'sl', 'sr', 'jl', 'jr', 'fl', 'fr']

    def fsm(self):
        self.machine.add_transition('run_left', 'sl', 'rl')
        self.machine.add_transition('run_left', 'sr', 'rl')
        self.machine.add_transition('run_left', 'fl', 'rl')
        self.machine.add_transition('run_left', 'rr', 'rl')
        self.machine.add_transition('run_right', 'sl', 'rr')
        self.machine.add_transition('run_right', 'sr', 'rr')
        self.machine.add_transition('run_right', 'fr', 'rr')
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

    def on_enter_rr(self):
        self.image = self.rabbit_run_right

    def on_enter_rl(self):
        self.image = self.rabbit_run_left

    def on_enter_sr(self):
        self.image = self.rabbit_still_right

    def on_enter_sl(self):
        self.image = self.rabbit_still_left

    def on_enter_fl(self):
        self.image = self.fall_left

    def on_enter_fr(self):
        self.image = self.fall_right

    def on_enter_jl(self):
        self.image = self.jump_left

    def on_enter_jr(self):
        self.image = self.jump_right

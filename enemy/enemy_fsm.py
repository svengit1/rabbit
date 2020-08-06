from transitions import Machine, MachineError

from enemy.enemy_animation import EnemyAnimation


class EnemyFSM():
    states = ['wl', 'wr', 'il', 'ir', 'al', 'ar', 'dl', 'dr']

    def fsm(self):
        self.machine.add_transition('walk_left', 'wl', 'wl')
        self.machine.add_transition('walk_left', 'wr', 'wl')
        self.machine.add_transition('walk_left', 'il', 'wl')
        self.machine.add_transition('walk_left', 'ir', 'wl')
        self.machine.add_transition('walk_left', 'ar', 'wl')
        self.machine.add_transition('walk_left', 'al', 'wl')

        self.machine.add_transition('walk_right', 'wl', 'wr')
        self.machine.add_transition('walk_right', 'wr', 'wr')
        self.machine.add_transition('walk_right', 'il', 'wr')
        self.machine.add_transition('walk_right', 'ir', 'wr')
        self.machine.add_transition('walk_right', 'ar', 'wr')
        self.machine.add_transition('walk_right', 'al', 'wr')

        self.machine.add_transition('attack', 'wl', 'al')
        self.machine.add_transition('attack', 'wr', 'al')
        self.machine.add_transition('attack', 'il', 'al')
        self.machine.add_transition('attack', 'ir', 'al')
        self.machine.add_transition('attack', 'wl', 'ar')
        self.machine.add_transition('attack', 'wr', 'ar')
        self.machine.add_transition('attack', 'il', 'ar')
        self.machine.add_transition('attack', 'ir', 'ar')

        self.machine.add_transition('killed', 'wl', 'dl')
        self.machine.add_transition('killed', 'il', 'dl')
        self.machine.add_transition('killed', 'al', 'dl')
        self.machine.add_transition('killed', 'wr', 'dr')
        self.machine.add_transition('killed', 'ir', 'dr')
        self.machine.add_transition('killed', 'ar', 'dr')

    def on_enter_wr(self):
        self.image = self.ea.get_animation(EnemyAnimation.WALK_RIGHT,
                                           duration=0.08,
                                           loop=True)

    def on_enter_wl(self):
        self.image = self.ea.get_animation(EnemyAnimation.WALK_LEFT,
                                           duration=0.08,
                                           loop=True)

    def on_enter_ir(self):
        self.image = self.ea.get_animation(EnemyAnimation.IDLE_RIGHT,
                                           duration=0.08,
                                           loop=True)

    def on_enter_il(self):
        self.image = self.ea.get_animation(EnemyAnimation.IDLE_LEFT,
                                           duration=0.08,
                                           loop=True)

    def on_enter_ar(self):
        self.image = self.ea.get_animation(EnemyAnimation.ATTACK_RIGHT,
                                           duration=0.08,
                                           loop=True)

    def on_enter_al(self):
        self.image = self.ea.get_animation(EnemyAnimation.ATTACK_LEFT,
                                           duration=0.08,
                                           loop=True)

    def on_enter_dr(self):
        self.image = self.ea.get_animation(EnemyAnimation.DEAD_RIGHT,
                                           duration=0.08,
                                           loop=True)

    def on_enter_dl(self):
        self.image = self.ea.get_animation(EnemyAnimation.DEAD_LEFT,
                                           duration=0.08,
                                           loop=True)

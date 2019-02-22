from fight.fsm import FSM


class DefaultUnit:

    machine = FSM()

    def __init__(self, name, hp, dam, attlen):
        self.name = name
        self.hp = hp
        self.dam = dam
        self.attlen = attlen

    def update(self, loop_time):
        self.machine.update(loop_time)

    def is_die(self):
        if self.hp < 0:
            handle_hero_die_event(self)
            return True
        return False


def handle_hero_die_event(hero):
    hero.machine.pause(hero)

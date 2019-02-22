from abc import abstractmethod, ABCMeta
from message_formatter import format_message


# 统一消息格式 hero|action|param 1|param 2|..|param n
class State(metaclass=ABCMeta):
    @abstractmethod
    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def update(self, loop_time):
        pass

    def handle_event(self, event):
        pass


class FSM:

    paused = False
    state = 0

    def set_state(self, state):
        self.state = state

    def change_state(self, state):
        if self.state != state:
            state.on_exit()
        self.state = state
        self.state.on_enter()

    def update(self, loop_time):
        if self.paused:
            return
        self.state.update(loop_time)

    def pause(self, hero):
        print(format_message("{0}|die", hero.name))
        self.change_state(IdleState(hero))
        self.paused = True


class IdleState(State):

    __cd = 1

    def __init__(self, hero):
        self.hero = hero

    def on_enter(self):
        print(format_message("{0} enter idleState", self.hero.name))
        print(format_message("{0}|ready", self.hero.name))

    def on_exit(self):
        print(format_message("{0} exit idleState", self.hero.name))

    def update(self, loop_time):
        hero = self.hero
        if self.__cd > 0:
            self.__cd -= loop_time
            return

        if hero.room.need_move(hero):
            x, y = hero.room.calc_move(hero)
            next_state = MoveState(hero, x, y)
            hero.machine.change_state(next_state)
        else:
            next_state = FightState(hero)
            hero.machine.change_state(next_state)


class MoveState(State):

    __move_cd = 0.5

    def __init__(self, machine, hero, last_pos, now_pos):
        self.machine = machine
        self.hero = hero
        self.last_pos = last_pos
        self.now_pos = now_pos
        self.__init()

    def on_enter(self):
        print(format_message("{0} enter moveState", self.hero.name))
        print(format_message("{0}|move|{1}|{2}", self.hero.name, self.last_pos, self.now_pos))

    def on_exit(self):
        print(format_message("{1} exit moveState", self.hero.name))

    def update(self, loop_time):
        if self.cd > 0:
            self.cd -= loop_time
            return
        hero = self.hero
        hero.room.move_succ(hero, self.now_pos)
        print(format_message("{0}|reach|{1}", self.hero.name, self.now_pos))
        hero.machine.change_state(IdleState(hero))

    def __init(self):
        self.cd = abs(self.now_pos - self.last_pos) * 0.5


class FightState(State):

    __cd = 0.5

    def __init__(self, hero):
        self.hero = hero

    def on_enter(self):
        print(format_message("{0} enter fightState", self.hero.name))
        print(format_message("{0}|readyFight", self.hero.name))

    def on_exit(self):
        pass
        print(format_message("{0} exit fightState", self.hero.name))

    def update(self, loop_time):
        if self.__cd > 0:
            self.__cd -= loop_time
            return
        hero = self.hero
        att_dir, min_d, target = hero.room.find_target(hero)
        if target is None:
            hero.machine.change_state(IdleState(hero))
        else:
            print(format_message("{0}|att|{1}|{2}|{3}", hero.name, target.name, hero.dam, target.hp))
            target.hp -= hero.dam
            self.__cd = 0.2





from fight.fsm import IdleState


class MultiFightRoom:

    MID_X = 10
    MOVE_TIME = 0.2

    def __init__(self, att_heroes, def_heroes):
        self.att_heroes = att_heroes
        self.def_heroes = def_heroes
        all_heroes = att_heroes + def_heroes
        for hero in all_heroes:
            hero.room = self
            hero.machine.set_state(IdleState(hero))
        self.all_pos = {hero: 0 for hero in all_heroes}

    def check_end(self):
        return self.att_heroes == [] or self.def_heroes == []

    def update(self, loop_time: float):
        if not started(self):
            self._init()
            return
        for hero in self.att_heroes + self.def_heroes:
            hero.update(loop_time)

    def _init(self):
        self.__start = True
        att_heroes = self.att_heroes
        def_heroes = self.def_heroes
        att_heroes.sort(key=lambda hero:hero.attlen)
        def_heroes.sort(key=lambda hero:hero.attlen)
        arrange_hero_pos(att_heroes, self.MID_X, -1)
        arrange_hero_pos(def_heroes, self.MID_X, 1)

    __start = False

    def get_start(self):
        return self.__start

    def move_success(self, hero, now_pos):
        self.all_pos[hero] = now_pos

    def need_move(self, hero):
        att_heroes = self.att_heroes
        def_heroes = self.def_heroes
        all_pos = self.all_pos
        if not started(self):
            return True
        if hero in att_heroes:
            for target in def_heroes:
                if all_pos[hero] + hero.attlen > all_pos[target] and not target.is_die():
                    return False
        else:
            for target in att_heroes:
                if all_pos[hero] - hero.attlen < all_pos[target] and not target.is_die():
                    return False
        return True

    def calc_move(self, hero):
        all_pos = self.all_pos
        my_pos = all_pos[hero]
        att_dir, min_d, target = self.find_target(hero)
        distance = 0 if min_d <= hero.attlen else min_d - hero.attlen
        new_pos = my_pos + att_dir * distance
        return [my_pos, new_pos]

    def find_target(self, hero):
        all_pos = self.all_pos
        my_pos = all_pos[hero]
        att_dir = 1 if hero in self.att_heroes else -1  # 方向
        min_d = 18
        target = hero
        for hero in all_pos.items():  # 找到离自己最近的攻击目标
            distance = min_d
            if att_dir > 0 and hero[0] in self.def_heroes and not hero[0].is_die():
                distance = abs(my_pos - hero[1])
            if att_dir < 0 and hero[0] in self.att_heroes and not hero[0].is_die():
                distance = abs(my_pos - hero[1])
            if min_d > distance:
                min_d = distance
                target = hero[0]
        return [att_dir, min_d, target]

    def __str__(self):
        print("\natt:" + str(self.att_heroes))
        print("\ndef:" + str(self.def_heroes))


def started(room) -> bool:
    return room.get_start()


def arrange_hero_pos(heroes, start, step):
    for hero in heroes:
        start -= step
        if hero.is_die():
            continue
        hero.room.all_pos[hero] = start

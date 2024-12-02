from utils import *


@dataclass(unsafe_hash=True)
class Boss:
    health: int
    damage: int

    def copy(self, health=None):
        return Boss(
            self.health if health is None else health,
            self.damage,
        )


@dataclass(unsafe_hash=True)
class Player:
    health: int = 50
    armor: int = 0
    mana: int = 500

    def copy(self, health=None, armor=None, mana=None):
        return Player(
            self.health if health is None else health,
            self.armor if armor is None else armor,
            self.mana if mana is None else mana,
        )


@dataclass(unsafe_hash=True)
class Effects:
    shield: int = 0
    poison: int = 0
    recharge: int = 0

    def apply(self, boss, player):
        if self.shield:
            player = player.copy(armor=7)
        else:
            player = player.copy(armor=0)
        if self.poison:
            boss = boss.copy(health=boss.health - 3)
        if self.recharge:
            player = player.copy(mana=player.mana + 101)
        return boss, player, self.dec()

    def dec(self):
        return Effects(max(0, self.shield - 1), max(0, self.poison - 1), max(0, self.recharge - 1))


def take_turns(action, boss, player, effects, spent):
    """returns the new state after the action is taken"""
    # hard mode (part 2)
    player = player.copy(health=player.health - 1)
    # player turn
    boss, player, effects = effects.apply(boss, player)
    if boss.health <= 0 or player.health <= 0:
        return boss, player, effects, spent
    match action:
        case "Magic Missile":
            spent += 53
            player = player.copy(mana=player.mana - 53)
            boss = boss.copy(health=boss.health - 4)
        case "Drain":
            spent += 73
            player = player.copy(mana=player.mana - 73)
            boss = boss.copy(health=boss.health - 2)
            player = player.copy(health=player.health + 2)
        case "Shield":
            spent += 113
            player = player.copy(mana=player.mana - 113)
            effects.shield = 6
        case "Poison":
            spent += 173
            player = player.copy(mana=player.mana - 173)
            effects.poison = 6
        case "Recharge":
            spent += 229
            player = player.copy(mana=player.mana - 229)
            effects.recharge = 5
    if boss.health <= 0 or player.health <= 0:
        return boss, player, effects, spent
    # boss turn
    boss, player, effects = effects.apply(boss, player)
    if boss.health <= 0 or player.health <= 0:
        return boss, player, effects, spent
    player = player.copy(health=player.health - max(1, boss.damage - player.armor))
    return boss, player, effects, spent


@cache
def fight(boss, player, effects, spent=0):
    """returns the minimum amount of mana necessary to win from this game state"""
    if boss.health <= 0:
        return spent
    if player.health <= 0:
        return inf
    # take each allowed action recursively
    magic_missile = inf if player.mana < 53 else fight(*take_turns("Magic Missile", boss, player, effects, spent))
    drain = inf if player.mana < 73 else fight(*take_turns("Drain", boss, player, effects, spent))
    shield = inf if effects.shield > 1 or player.mana < 113 else fight(*take_turns("Shield", boss, player, effects, spent))
    poison = inf if effects.poison > 1 or player.mana < 173 else fight(*take_turns("Poison", boss, player, effects, spent))
    recharge = inf if effects.recharge > 1 or player.mana < 229 else fight(*take_turns("Recharge", boss, player, effects, spent))
    return min(magic_missile, drain, shield, poison, recharge)


def solve(input):
    boss = split(input, "\n", ": ").map(t(lambda stat, value: int(value))).tuple()
    return fight(Boss(*boss), Player(50, 0, 500), Effects())


with print_duration():
    print("solution:", solve(read("input.txt")))

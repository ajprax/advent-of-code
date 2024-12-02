from utils import *


# (cost, damage, armor)
shop = dict(
    weapons=dict(
        Dagger=(8, 4, 0),
        Shortsword=(10, 5, 0),
        Warhammer=(25, 6, 0),
        Longsword=(40, 7, 0),
        Greataxe=(74, 8, 0),
    ),
    armor=dict(
        Leather=(13, 0, 1),
        Chainmail=(31, 0, 2),
        Splintmail=(53, 0, 3),
        Bandedmail=(75, 0, 4),
        Platemail=(102, 0, 5),
    ),
    rings=dict(
        Damage1=(25, 1, 0),
        Damage2=(50, 2, 0),
        Damage3=(100, 3, 0),
        Defense1=(20, 0, 1),
        Defense2=(40, 0, 2),
        Defense3=(80, 0, 3),
    )
)


def purchase(weapon, armor=None, rings=()):
    cda = np.array([0, 0, 0])
    cda += shop["weapons"][weapon]
    cda += shop["armor"][armor] if armor else 0
    for ring in rings:
        cda += shop["rings"][ring]
    return tuple(cda)


def fight(player, boss):
    ph, pd, pa = player
    bh, bd, ba = boss
    while True:
        bh -= max(1, pd - ba)
        if bh <= 0:
            return True
        ph -= max(1, bd - pa)
        if ph <= 0:
            return False


def solve(input):
    boss = split(input, "\n", ": ").map(t(lambda stat, value: int(value)))
    weapons = List(shop["weapons"])
    armor = List(shop["armor"]) + [None]
    rings = List(shop["rings"]).combinations(2).list() + List(shop["rings"]).map(lambda ring: [ring]) + [()]
    for cost, damage, armor in weapons.product(armor, rings).map(t(purchase)).list().sorted():
        if fight([100, damage, armor], boss):
            return cost


with print_duration():
    print("solution:", solve(read("input.txt")))

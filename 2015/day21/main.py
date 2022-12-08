import sys
import time
import re
import math
import itertools
import numpy as np

class Item:
    def __init__(self, cost, damage, armor):
        self.cost = cost
        self.damage = damage
        self.armor = armor

# shared variables here
WEAPONS = {
    "dagger": Item(8, 4, 0),
    "shortsword": Item(10, 5, 0),
    "warhammer": Item(25, 6, 0),
    "longsword": Item(40, 7, 0),
    "greataxe": Item(74, 8, 0)
}

ARMOR = {
    "none": Item(0, 0, 0),
    "leather": Item(13, 0, 1),
    "chainmail": Item(31, 0, 2),
    "splintmail": Item(53, 0, 3),
    "bandedmail": Item(75, 0, 4),
    "platemail": Item(102, 0, 5)
}

RINGS = {
    "none": Item(0, 0, 0),
    "damage +1": Item(25, 1, 0),
    "damage +2": Item(50, 2, 0),
    "damage +3": Item(100, 3, 0),
    "defense +1": Item(20, 0, 1),
    "defense +2": Item(40, 0, 2),
    "defense +3": Item(80, 0, 3)
}

boss_hp = 100
boss_damage = 8
boss_armor = 2
# boss_hp = 12
# boss_damage = 7
# boss_armor = 2

def player_wins(weapon, armor, rings):
    player_hp = 100
    player_damage = weapon.damage
    player_armor = armor.armor if armor != None else 0
    if len(rings) > 0:
        player_damage += sum([ring.damage for ring in rings])
        player_armor += sum([ring.armor for ring in rings])

    player_reduced_damage = boss_damage - player_armor
    boss_reduced_damage = player_damage - boss_armor
    player_hits_to_lose = max(1, math.ceil(player_hp / max(1, player_reduced_damage))) 
    boss_hits_to_lose = max(1, math.ceil(boss_hp / max(1, boss_reduced_damage))) 
    # <= because player goes first, so if they both take the same number of turns the player will win
    return boss_hits_to_lose <= player_hits_to_lose

# part 1, takes in lines of file
def p1(lines):
    costs = []
    ring_combinations = itertools.combinations(RINGS.keys(), 2)
    ring_combinations = [comb for comb in ring_combinations if comb[0] != comb[1]]
    for weapon in WEAPONS.keys():
        for armor in ARMOR.keys():
            for rings in ring_combinations:
                weapon_item = WEAPONS[weapon]
                armor_item = ARMOR[armor]
                ring_items = [RINGS[ring] for ring in rings]
                if player_wins(weapon_item, armor_item, ring_items):
                    costs.append(weapon_item.cost + armor_item.cost + sum([ring_item.cost for ring_item in ring_items]))

    return min(costs)

# part 2, takes in lines of file
def p2(lines):
    costs = []
    ring_combinations = itertools.combinations(RINGS.keys(), 2)
    ring_combinations = [comb for comb in ring_combinations if comb[0] != comb[1]]
    for weapon in WEAPONS.keys():
        for armor in ARMOR.keys():
            for rings in ring_combinations:
                weapon_item = WEAPONS[weapon]
                armor_item = ARMOR[armor]
                ring_items = [RINGS[ring] for ring in rings]
                if not player_wins(weapon_item, armor_item, ring_items):
                    costs.append(weapon_item.cost + armor_item.cost + sum([ring_item.cost for ring_item in ring_items]))

    return max(costs)

filename = "input.txt"

if "test" in sys.argv:
    filename = "test.txt"

def format_time(time_ns):
    names = ["hr", "m", "s", "ms", "µs", "ns"]
    names.reverse()
    times = [
        time_ns % 1000,
        (time_ns // 1000) % 1000,
        (time_ns // (1000 * 10**3)) % 1000,
        (time_ns // (1000 * 10**6)) % 60,
        (time_ns // (1000 * 10**6) // 60) % 60,
        (time_ns // (1000 * 10**6) // 60 // 60) % 60
    ]
    for i in range(0, len(times)):
        if i < len(times) - 1:
            if times[i + 1] == 0:
                return "%s%s " % (times[i], names[i])
        else:
            return "%s%s " % (times[i], names[i])

with open(filename, "r") as f:
    lines = f.readlines()
    t = time.perf_counter_ns()
    a = p1(lines)
    dur = time.perf_counter_ns() - t

    print("\033[0;33m├ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

    t = time.perf_counter_ns()
    a = p2(lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

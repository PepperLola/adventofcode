import sys
import time
import re
import itertools
import numpy as np
from functools import cache
from collections import namedtuple

Game = namedtuple("Game", [
    "player_hp",
    "player_armor",
    "player_mana",
    "boss_hp",
    "boss_damage",
    "shield_counter",
    "poison_counter",
    "recharge_counter",
    "player_turn",
    "hard_mode"
])

MANA_MAGIC_MISSILE = 53
MANA_DRAIN = 73
MANA_SHIELD = 113
MANA_POISON = 173
MANA_RECHARGE = 229

def cast_magic_missile(game):
    return game._replace(boss_hp=game.boss_hp - 4, player_mana=game.player_mana - MANA_MAGIC_MISSILE)

def cast_drain(game):
    return game._replace(boss_hp=game.boss_hp - 2, player_hp=game.player_hp + 2, player_mana=game.player_mana - MANA_DRAIN)

def cast_shield(game):
    return game._replace(
        player_armor=7,
        shield_counter=6,
        player_mana=game.player_mana - MANA_SHIELD
    )

def cast_poison(game):
    return game._replace(
        poison_counter=6,
        player_mana=game.player_mana - MANA_POISON
    )

def cast_recharge(game):
    return game._replace(
        recharge_counter=5,
        player_mana=game.player_mana - MANA_RECHARGE
    )

def counters(game):
    if game.shield_counter > 0:
        game = game._replace(shield_counter=game.shield_counter - 1)
        if game.shield_counter == 0:
            game = game._replace(player_armor=0)

    if game.poison_counter > 0:
        game = game._replace(boss_hp=game.boss_hp - 3, poison_counter=game.poison_counter - 1)

    if game.recharge_counter > 0:
        game = game._replace(player_mana=game.player_mana + 101, recharge_counter=game.recharge_counter - 1)

    return game

def boss_attack(game):
    return game._replace(
        player_hp=game.player_hp - max(1, game.boss_damage - game.player_armor)
    )

def change_turn(game):
    return game._replace(player_turn=not game.player_turn)

def game_over(game):
    return game.boss_hp <= 0 or game.player_hp <= 0

def player_wins(game):
    return game.boss_hp <= 0

# shared variables here
boss_hp = 55
boss_damage = 8

@cache
def get_next_best(game):
    if player_wins(game):
        return 0
    elif game_over(game):
        return -1

    game = change_turn(game)

    if game.player_turn and game.hard_mode:
        game = game._replace(player_hp=game.player_hp - 1)
        if game_over(game):
            return -1

    game = counters(game)

    if game_over(game):
        return 0

    if game.player_turn:
        options = []
        if game.player_mana >= MANA_MAGIC_MISSILE:
            options.append((get_next_best(cast_magic_missile(game)), MANA_MAGIC_MISSILE))
        if game.player_mana >= MANA_DRAIN:
            options.append((get_next_best(cast_drain(game)), MANA_DRAIN)) #includes both to add mana spent this turn to total
        if game.player_mana >= MANA_SHIELD and game.shield_counter == 0:
            options.append((get_next_best(cast_shield(game)), MANA_SHIELD))
        if game.player_mana >= MANA_POISON and game.poison_counter == 0:
            options.append((get_next_best(cast_poison(game)), MANA_POISON))
        if game.player_mana >= MANA_RECHARGE and game.recharge_counter == 0:
            options.append((get_next_best(cast_recharge(game)), MANA_RECHARGE))

        if len(options) == 0: #cannot attack
            return -1 # lose
        elif all(o[0] == -1 for o in options):
            return -1
        else:
            return min(sum(o) for o in options if o[0] >= 0)

    return get_next_best(boss_attack(game))

# part 1, takes in lines of file
def p1(lines):
    game = Game(50, 0, 500, boss_hp, boss_damage, 0, 0, 0, False, False)
    return get_next_best(game)

# part 2, takes in lines of file
def p2(lines):
    game = Game(50, 0, 500, boss_hp, boss_damage, 0, 0, 0, False, True)
    return get_next_best(game)

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

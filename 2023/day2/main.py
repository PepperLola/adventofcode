import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid

games = []

# part 1, takes in lines of file
def p1(file, content, lines):
    max_col = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    colors = max_col.keys()
    id_sum = 0
    # construct games
    for line in lines:
        game = re.search(r"Game (\d+):", line).group(1)
        line = line.replace("Game " + game + ": ", "")
        sets = line.split("; ")
        game_sets = []
        for s in sets:
            game_set = []
            split = s.split(", ")
            for s2 in split:
                s3 = s2.split(" ")
                game_set.append((int(s3[0]), s3[1]))
            game_sets.append(game_set)
        games.append((int(game), game_sets))

    for game in games:
        valid = True
        for game_set in game[1]:
            if not valid:
                break
            for cube in game_set:
                if not valid:
                    break
                if cube[1] in colors and int(cube[0]) > max_col[cube[1]]:
                    valid = False
        if valid:
            id_sum += game[0]

    return id_sum

# part 2, takes in lines of file
def p2(file, content, lines):
    total = 0
    for game in games:
        mins = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        colors = mins.keys()
        for game_set in game[1]:
            for cube in game_set:
                cube_val = cube[0]
                if cube[1] in colors and cube_val > mins[cube[1]]:
                    mins[cube[1]] = cube_val
        total += mins["red"] * mins["green"] * mins["blue"]

    return total 

filename = "input.txt"

if "test" in sys.argv:
    filename = "test.txt"

with open(filename, "r") as f:
    content = f.read()
    lines = content.splitlines()
    t = time.perf_counter_ns()
    a = p1(f, content, lines)
    dur = time.perf_counter_ns() - t

    print("\033[0;33m├ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

    t = time.perf_counter_ns()
    a = p2(f, content, lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

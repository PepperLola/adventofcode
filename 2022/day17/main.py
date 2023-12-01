import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np

# shared variables here
rocks = [
    [
        [1, 1, 1, 1]
    ],
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 1]
    ],
    [
        [1],
        [1],
        [1],
        [1]
    ],
    [
        [1, 1],
        [1, 1]
    ]
]

rock_max_col = [
    [1, 1, 1, 1],
    [2, 3, 2],
    [1, 1, 3],
    [4],
    [2, 2]
]

top_solid = [0, 0, 0, 0, 0, 0, 0]

current_rock = 0
curr_x = 2
curr_y = 3

def check_hit_block(x_off = 0, y_off = 0):
    global curr_x, curr_y
    rock = rocks[current_rock]
    for y in range(0, len(rock)):
        for x in range(0, len(rock[y])):
            if rock[y][x] == 1:
                if top_solid[curr_x + x + x_off] >= curr_y + y_off + y:
                    return True

def handle_move(move):
    global curr_x, curr_y
    if move == "<" and curr_x > 0 and not check_hit_block(-1):
        curr_x -= 1
    elif move == ">":
        for y in range(0, len(rocks[current_rock])):
            for x in range(0, len(rocks[current_rock][y])):
                if rocks[current_rock][y][x] == 1:
                    if curr_x + x >= 6:
                        return
        if not check_hit_block(1):
            curr_x += 1

def handle_fall():
    global curr_y
    if not check_hit_block(0, -1):
        curr_y -= 1

# part 1, takes in lines of file
def p1(lines):
    global curr_x, curr_y, current_rock, top_solid
    line = lines[0]
    curr_inst = 0

    while curr_inst < len(line):
        print(f"({curr_x}, {curr_y})", "ROCK", current_rock, "SOLID", top_solid, "INST", curr_inst)
        input()
        if check_hit_block(0, -1):
            curr_inst += 1
            handle_move(line[curr_inst])
            curr_y -= 1
            # find max under rock and add column to that max
            for x in range(0, len(rocks[current_rock][0])):
                top_solid[curr_x + x] += rock_max_col[current_rock][x]
            current_rock += 1
            curr_x = 2
            curr_y = max(top_solid) + 3
        else:
            handle_move(line[curr_inst])
            handle_fall()
        curr_inst += 1

    return max(top_solid)

# part 2, takes in lines of file
def p2(lines):
    return 0

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
    lines = f.read().splitlines()
    t = time.perf_counter_ns()
    a = p1(lines)
    dur = time.perf_counter_ns() - t

    print("\033[0;33m├ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

    t = time.perf_counter_ns()
    a = p2(lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

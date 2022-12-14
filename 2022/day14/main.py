import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np

# shared variables here
def sign(x):
    return int(math.copysign(1, x))

def parse_cave(lines):
    rocks = defaultdict(int)
    highest_y = -1
    for line in lines:
        s = line.split(" -> ")
        start = s[0].split(",")
        for pt in s[1:]:
            end = pt.split(",")
            x_start = int(start[0])
            y_start = int(start[1])
            x_diff = int(end[0]) - x_start
            y_diff = int(end[1]) - y_start
            if y_start + y_diff > highest_y:
                highest_y = y_start + y_diff
            if x_diff == 0:
                if y_diff > 0:
                    for y in range(0, y_diff + 1):
                        rocks[(x_start, y_start + y)] = 1
                elif y_diff < 0:
                    for y in range(abs(y_diff), -1, -1):
                        rocks[(x_start, y_start - y)] = 1
            elif y_diff == 0:
                if x_diff > 0:
                    for x in range(0, x_diff + 1):
                        rocks[(x_start + x, y_start)] = 1
                elif x_diff < 0:
                    for x in range(abs(x_diff), -1, -1):
                        rocks[(x_start - x, y_start)] = 1
            start = end
    return (rocks, highest_y)

# part 1, takes in lines of file
def p1(lines):
    rocks, highest_y = parse_cave(lines)

    sand_in_abyss = False
    sand_falling = False
    sand_pos = (500, 0)
    i = 0

    while not sand_in_abyss:
        if sand_falling:
            next_sand_pos = (sand_pos[0], sand_pos[1] + 1)
            if rocks[next_sand_pos] > 0:
                next_sand_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
                if rocks[next_sand_pos] > 0:
                    next_sand_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
                    if rocks[next_sand_pos] > 0:
                        next_sand_pos = sand_pos
                        rocks[sand_pos] = 2
                        sand_falling = False
            if next_sand_pos[1] > highest_y:
                sand_in_abyss = True
                return i - 1
            sand_pos = next_sand_pos
            continue
        i += 1
        sand_pos = (500, 0)
        sand_falling = True

    return 0

# part 2, takes in lines of file
def p2(lines):
    rocks, highest_y = parse_cave(lines)

    for x in range(250, 750):
        rocks[(x, highest_y + 2)] = 1

    sand_in_abyss = False
    sand_falling = False
    sand_pos = (500, 0)
    i = 0

    while rocks[(500, 0)] != 2:
        if sand_falling:
            next_sand_pos = (sand_pos[0], sand_pos[1] + 1)
            if rocks[next_sand_pos] > 0:
                next_sand_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
                if rocks[next_sand_pos] > 0:
                    next_sand_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
                    if rocks[next_sand_pos] > 0:
                        next_sand_pos = sand_pos
                        rocks[sand_pos] = 2
                        sand_falling = False
            sand_pos = next_sand_pos
        else:
            i += 1
            sand_pos = (500, 0)
            sand_falling = True

    return i

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

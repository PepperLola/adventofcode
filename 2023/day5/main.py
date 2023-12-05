import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid

# shared variables here
maps = []

# part 1, takes in lines of file
def p1(file, content, lines):
    lq = deque(lines)
    seeds = [int(i) for i in lines[0][7:].split(" ")]
    lq.popleft()
    while lq[0].strip() == "":
        lq.popleft()
    while len(lq) > 0:
        lq.popleft()
        maps.append([])
        while len(lq) > 0 and lq[0].strip() != "":
            left = lq.popleft()
            maps[-1].append([int(i) for i in left.strip().split(" ")])
        if len(lq) > 0:
            lq.popleft()
    positions = []
    for seed in seeds:
        for map in maps:
            for rng in map:
                if rng[1] <= seed <= rng[1]+rng[2]:
                    seed = rng[0]+(seed-rng[1])
                    break
        positions.append(seed)
    return min(positions)

# part 2, takes in lines of file
def p2(file, content, lines):
    seeds = [int(i) for i in lines[0][7:].split(" ")]
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append([])
        seed_ranges[-1] = [seeds[i], seeds[i+1]]
    maps.reverse()
    for i in itertools.count():
        seed = i
        for map in maps:
            for rng in map:
                if rng[0] <= seed < rng[0]+rng[2]:
                    seed = rng[1]+(seed-rng[0])
                    break
        for rng in seed_ranges:
            if rng[0] <= seed < rng[0]+rng[1]:
                return i
    return -1

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

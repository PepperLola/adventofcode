import sys
import time
import re
import itertools
from collections import defaultdict, deque
from matplotlib.path import Path
import math
import copy
import numpy as np
from util import format_time, number_grid

# shared variables here
def find_adjacent(x, y, map):
    valid = []
    if x < len(map[0])-1 and map[y][x+1] in ["-", "J", "7"] and map[y][x] in "-LFS":
        valid.append((x+1, y))
    if x > 0 and map[y][x-1] in ["-", "F", "L"] and map[y][x] in "-J7S":
        valid.append((x-1, y))
    if y < len(map)-1 and map[y+1][x] in "|LJ" and map[y][x] in "|7FS":
        valid.append((x, y+1))
    if y > 0 and map[y-1][x] in "|F7" and map[y][x] in "|LJS":
        valid.append((x, y-1))

    return valid

def bfs(map, start_pos) -> list[tuple[int, int]]:
    x, y = start_pos
    visited = []
    queue = deque([(x, y)])
    while len(queue):
        pos = queue.popleft()
        if pos in visited:
            continue
        visited.append(pos)
        for adj in find_adjacent(pos[0], pos[1], map):
            if adj not in visited:
                queue.append(adj)
    return visited

start_pos = None
found = []
map = []

# part 1, takes in lines of file
def p1(file, content, lines):
    global start_pos
    global found
    global map
    map = [list(line) for line in lines]
    for (i, line) in enumerate(map):
        for (j, c) in enumerate(line):
            if c == "S":
                start_pos = (j, i)
                break
    found = bfs(map, start_pos)
    return len(found) // 2


# part 2, takes in lines of file
def p2(file, content, lines):
    within = 0
    for y in range(len(map)):
        num_to_left = 0
        for x in range(len(map[0])):
            if (x, y) in found:
                if map[y][x] in "JL|S":
                    num_to_left += 1
                continue
            if num_to_left % 2 == 1:
                within += 1
    return within

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

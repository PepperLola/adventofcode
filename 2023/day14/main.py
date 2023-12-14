import sys
import time
import re
import itertools
import functools
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid

# shared variables here
def find_cube_above(grid, x, y):
    for y2 in range(y-1, -1, -1):
        if y2 < 0: break
        if grid[y2][x] in "O#":
            return (x, y2)
    return (x,-1)

def find_cube_right(grid, x, y):
    for x2 in range(x+1, len(grid[0])):
        if x2 >= len(grid[0]): break
        if grid[y][x2] in "O#":
            return (x2, y)
    return (len(grid[0]), y)

def find_cube_below(grid, x, y):
    for y2 in range(y+1, len(grid)):
        if y2 >= len(grid): break
        if grid[y2][x] in "O#":
            return (x, y2)
    return (x, len(grid))

def find_cube_left(grid, x, y):
    for x2 in range(x-1, -1, -1):
        if x2 < 0: break
        if grid[y][x2] in "O#":
            return (x2, y)
    return (-1, y)

def run_slide(grid, direction):
    # direction = 0 up, 1 left, 2 down, 3 right
    if direction == 0:
        for (y, line) in enumerate(grid):
            for (x, c) in enumerate(list(line)):
                if c == "O":
                    grid[y][x] = "."
                    x2, y2 = find_cube_above(grid, x, y)
                    grid[y2+1][x2] = "O"
    elif direction == 1:
        for (y, line) in enumerate(grid):
            for (x, c) in enumerate(list(line)):
                if c == "O":
                    grid[y][x] = "."
                    x2, y2 = find_cube_left(grid, x, y)
                    grid[y2][x2+1] = "O"
    elif direction == 2:
        for y in range(len(grid)-1, -1, -1):
            line = grid[y]
            for (x, c) in enumerate(list(line)):
                if c == "O":
                    grid[y][x] = "."
                    x2, y2 = find_cube_below(grid, x, y)
                    grid[y2-1][x2] = "O"
    elif direction == 3:
        for x in range(len(grid[0])-1, -1, -1):
            for y in range(len(grid)-1, -1, -1):
                c = grid[y][x]
                if c == "O":
                    grid[y][x] = "."
                    x2, y2 = find_cube_right(grid, x, y)
                    grid[y2][x2-1] = "O"
    return grid

def score(grid):
    total = 0
    for (y, line) in enumerate(grid):
        for (x, c) in enumerate(line):
            if c == "O":
                total += (len(grid)-y)
    return total

# part 1, takes in lines of file
def p1(file, content, lines):
    total = 0
    grid = []
    for line in lines:
        grid.append(list(line))
    for (y, line) in enumerate(lines):
        for (x, c) in enumerate(list(line)):
            if c == "O":
                grid[y][x] = "."
                x2, y2 = find_cube_above(grid, x, y)
                grid[y2+1][x2] = "O"
    for (y, line) in enumerate(grid):
        for c in list(line):
            if c == "O":
                total += (len(grid)-y)
    return total

# part 2, takes in lines of file
def p2(file, content, lines):
    total = 0
    grid = []
    for line in lines:
        grid.append(list(line))
    cycles = 1000000000
    CACHE = {}
    for i in itertools.count(1):
        for dir in range(4):
            grid = run_slide(grid, dir)
        key = "".join(["".join(row) for row in grid])
        if key in CACHE:
            cycle_len = i - CACHE[key][0]
            for i2, v in CACHE.values():
                if i2 >= CACHE[key][0] and i2 % cycle_len == cycles % cycle_len:
                    return v
            break
        CACHE[key] = (i, score(grid))

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

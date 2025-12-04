from functools import cache
import sys
import time
import re
import itertools
from collections import defaultdict, deque, Counter
import math
import copy
import numpy as np
import networkx as nx
from util import format_time, letter_grid, number_grid

# shared variables here
g, gw, gh = [[]], 0, 0

ds = list(itertools.product([-1, 0, 1], [-1, 0, 1]))

def adj(grid, W, H, x, y):
    global ds
    ret = 0
    for (dx, dy) in ds:
        if dx == 0 and dy == 0:
            continue
        if 0 <= x + dx <= W-1 and 0 <= y + dy <= H-1:
            ret += 1 if (grid[y+dy][x+dx] == "@") else 0
    return ret

# part 1, takes in lines of file
def p1(file, content, lines: list[str]):
    global g, gw, gh
    g = letter_grid(lines)
    gw = len(g[0])
    gh = len(g)
    ret = 0
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if adj(g, gw, gh, x, y) < 4:
                ret += 1 if c == "@" else 0
    return ret

# part 2, takes in lines of file
def p2(file, content, lines: list[str]):
    global g, gw, gh
    ret = 0
    last_val = -1
    times_last = 0
    while True:
        for y, row in enumerate(g):
            for x, c in enumerate(row):
                if adj(g, gw, gh, x, y) < 4:
                    ret += 1 if c == "@" else 0
                    g[y][x] = "."
        if ret == last_val:
            times_last += 1
        else:
            times_last = 0
        if times_last == 3:
            return ret
        last_val = ret

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

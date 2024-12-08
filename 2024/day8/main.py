import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
import networkx as nx
from util import format_time, number_grid

# shared variables here
antennas = {}
W = 0
H = 0

# part 1, takes in lines of file
def p1(file, content, lines):
    global antennas, W, H
    x = 0
    y = 0
    W = len(lines[0])
    H = len(lines)
    for line in lines:
        x = 0
        for c in line:
            if c != ".":
                if c in antennas.keys():
                    antennas[c].append((x, y))
                else:
                    antennas[c] = [(x, y)]
            x += 1
        y += 1
    ret = set()
    for an in antennas.keys():
        combs = itertools.combinations(antennas[an], 2)
        for comb in combs:
            a1, a2 = comb
            x1, y1 = a1
            x2, y2 = a2

            dx = (x2 - x1)
            dy = (y2 - y1)
            if 0 <= x2 + dx < W and 0 <= y2 + dy < H:
                ret.add((x2+dx, y2+dy))
            if 0 <= x1 - dx < W and 0 <= y1 - dy < H:
                ret.add((x1-dx,y1-dy))
    return len(ret)

# part 2, takes in lines of file
def p2(file, content, lines):
    global antennas, W, H
    ret = set()
    for an in antennas.keys():
        combs = itertools.combinations(antennas[an], 2)
        for comb in combs:
            a1, a2 = comb
            x1, y1 = a1
            x2, y2 = a2

            dx = (x2 - x1)
            dy = (y2 - y1)
            while 0 <= x1 < W and 0 <= y1 < H:
                ret.add((x1, y1))
                x1 -= dx
                y1 -= dy
            while 0 <= x2 < W and 0 <= y2 < H:
                ret.add((x2, y2))
                x2 += dx
                y2 += dy
    return len(ret)

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

import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
import networkx as nx
from util import format_time, number_grid, letter_grid

# shared variables here
grid = []
start = (0, 0)
W = 0
H = 0

# part 1, takes in lines of file
def p1(file, content, lines):
    global grid, start, W, H
    grid = letter_grid(lines)
    start = (0, 0)
    H = len(grid)
    W = len(grid[0])
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "^":
                start = (x, y)
    pos = start
    dir = 0
    offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    path = set()
    path.add(pos)
    while True:
        off = offsets[dir]
        nx, ny = pos[0] + off[0], pos[1] + off[1]
        if nx >= 0 and nx < W and ny >= 0 and ny < H:
            if grid[ny][nx] == "#":
                dir += 1
                dir = dir % len(offsets)
            else:
                pos = (nx, ny)
                path.add(pos)
        else:
            break
    return len(path)


# part 2, takes in lines of file
def p2(file, content, lines):
    global grid, start, W, H
    offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    ret = set()
    for y in range(H):
        for x in range(W):
            dir = 0
            pos = start
            blockages = set() 
            old = grid[y][x]
            grid[y][x] = "#"
            while True:
                off = offsets[dir]
                nx, ny = pos[0] + off[0], pos[1] + off[1]
                if nx >= 0 and nx < W and ny >= 0 and ny < H:
                    if grid[ny][nx] == "#":
                        if (pos[0], pos[1], dir) in blockages:
                            ret.add((x, y))
                            break
                        blockages.add((pos[0], pos[1], dir))
                        dir += 1
                        dir = dir % len(offsets)
                    else:
                        pos = (nx, ny)
                else:
                    break
            grid[y][x] = old
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

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
dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]

def step(coord):
    return ( coord[0]+dx[coord[2]], coord[1]+dy[coord[2]], coord[2] )

def solve(g, coords):
    tiles = set()
    done = set()
    while len(coords) > 0:
        new_coords = []
        for coord in coords:
            if coord[0] >= len(g[0]) or coord[1] >= len(g) or coord[0] < 0 or coord[1] < 0:
                continue
            if not (coord[0], coord[1]) in tiles:
                tiles.add((coord[0], coord[1]))
            if coord in done:
                continue
            done.add(coord)
            dir = coord[2]

            c = g[coord[1]][coord[0]]
            if c == ".":
                new_coords.append(step(coord))
            elif c == "/":
                new_coords.append(step((coord[0], coord[1], {0:1, 1:0, 2:3, 3:2}[coord[2]])))
            elif c == "\\":
                new_coords.append(step((coord[0], coord[1], {0:3, 1:2, 2:1, 3:0}[coord[2]])))
            elif c == "-":
                if dir in [0, 2]:
                    new_coords.append(step(( coord[0], coord[1], 1 )))
                    new_coords.append(step(( coord[0], coord[1], 3 )))
                else:
                    new_coords.append(step(coord))
            elif c == "|":
                if dir in [1, 3]:
                    new_coords.append(step(( coord[0], coord[1], 0 )))
                    new_coords.append(step((coord[0], coord[1], 2)))
                else:
                    new_coords.append(step(coord))
        coords = new_coords
    return tiles

# part 1, takes in lines of file
def p1(file, content, lines):
    g = [list(line) for line in lines]
    # dir 0 = up, 1 = right, 2 = down, 3 = left
    coords = [( 0, 0, 1 )]

    return len(solve(g, coords))

# part 2, takes in lines of file
def p2(file, content, lines):
    g = [list(line) for line in lines]
    configs = {}
    for x in range(len(g[0])):
        coord = ( x, 0, 2 )
        configs[coord] = solve(g, [ coord ])
        coord = (x, len(g)-1, 0)
        configs[coord] = solve(g, [ coord ])
    for y in range(len(g)):
        coord = (0, y, 1)
        configs[coord] = solve(g, [ coord ])
        coord = (len(g[0])-1, y, 3)
        configs[coord] = solve(g, [ coord ])
    max = 0
    for coord in configs.keys():
        n = len(configs[coord])
        if n > max:
            max = n
    return max

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

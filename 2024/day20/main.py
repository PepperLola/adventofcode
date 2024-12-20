import sys
import time
import re
import itertools
from collections import defaultdict, deque, Counter
import math
import copy
import numpy as np
import networkx as nx
from util import format_time, number_grid

# shared variables here
g = nx.Graph()
W = 0
H = 0
shortest_path = {}

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def cheat_end(x, y, dist, lines):
    ret = []
    for dy in range(-dist, dist+1):
        rest = dist - abs(dy)
        for dx in range(-rest, rest+1):
            nx, ny = x+dx, y+dy
            if nx == x and ny == y:
                continue
            if 0 <= nx < W and 0 <= ny < H and lines[ny][nx] != "#":
                ret.append((nx, ny))
    return ret

# part 1, takes in lines of file
def p1(file, content, lines):
    global g, start, end, W, H, shortest_path
    W = len(lines[0])
    H = len(lines)
    end = ()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "E":
                end = (x, y)

            if c != "#":
                g.add_node((x, y))

                if x > 0 and lines[y][x-1] != "#":
                    g.add_edge((x, y), (x-1, y))
                if y > 0 and lines[y-1][x] != "#":
                    g.add_edge((x, y), (x, y-1))

    # convert path array to dict with node as key and position as value for fast distance lookup (found on reddit, ty)
    shortest_path = dict(nx.shortest_path_length(g, target=end))

    ret = 0
    for x, y in g.nodes:
        for rx, ry in cheat_end(x, y, 2, lines):
            dist = abs(rx-x) + abs(ry-y)
            saved = shortest_path[(x, y)] - shortest_path[(rx, ry)] - dist
            ret += saved >= 100
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    ret = 0
    for x, y in g.nodes:
        for rx, ry in cheat_end(x, y, 20, lines):
            dist = abs(rx-x) + abs(ry-y)
            saved = shortest_path[(x, y)] - shortest_path[(rx, ry)] - dist
            ret += saved >= 100
    return ret

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

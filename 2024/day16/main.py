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
import heapq

# shared variables here
grid = []
g = nx.Graph()
start = (0, 0)
end = (0, 0)
dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]
sd = 3
path = defaultdict(lambda: set())

def neighbors(pos):
    x, y, d = pos
    yield 1000, (x, y, (d-1) % 4)
    yield 1000, (x, y, (d+1) % 4)

    dx, dy = dirs[d]
    nx, ny = x + dx, y + dy
    if grid[nx][ny] != "#":
        yield 1, (nx, ny, d)

def traverse():
    global start, end, dists, path
    sx, sy = start
    s = (sx, sy, sd)
    pq = []
    p1 = None
    heapq.heappush(pq, (0, s))
    dists = defaultdict(lambda : float("inf"))
    while len(pq) > 0:
        dist, cur = heapq.heappop(pq)
        if cur[:2] == end:
            if p1 is None:
                p1 = dist
        for d, n in neighbors(cur):
            if dist + d < dists[n]:
                dists[n] = dist + d
                path[n] = {cur}
                heapq.heappush(pq, (dists[n], n))
            elif dist + d == dists[n]:
                path[n].add(cur)
    return p1

# part 1, takes in lines of file
def p1(file, content, lines):
    global grid, g, start, end, sd
    grid = letter_grid(lines)
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "S":
                start = (c, r)
            elif cell == "E":
                end = (c, r)
    # start is always bottom left
    # I think there is only ever one direction from start?
    sd = 2 if grid[start[1]-1][start[0]] != "#" else 3
    return traverse()

# part 2, takes in lines of file
def p2(file, content, lines):
    global path, end
    pos = (end[0], end[1], 1)
    ret = set([pos])
    q = deque([pos])
    while len(q):
        next = q.pop()
        for p in path[next]:
            if not p in ret:
                q.append(p)
                ret.add(p)
    return len(set(r[:2] for r in ret))

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

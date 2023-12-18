import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
import networkx
from util import format_time, number_grid
from heapq import heappush, heappop

# shared variables here
dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
grid = None

def neighbors(g, pos, ultra):
    x, y, in_dir, dir = pos
    dx, dy = dirs[dir]
    left, right = (-dy, dx), (dy, -dx)
    if in_dir < (10 if ultra else 3) and 0 <= x+dx < len(g[0]) and 0 <= y+dy < len(g):
        yield (x+dx, y+dy, in_dir+1, dir), int(g[y+dy][x+dx])
    for dx2, dy2 in left, right:
        if (not ultra or in_dir > 3) and 0 <= x+dx < len(g[0]) and 0 <= y+dy < len(g):
            yield (x+dx, y+dy, 1, dirs.index((dx2, dy2))), int(g[y+dy][x+dx])

def dijkstra(g, ultra=False):
    visited = set()
    start = (0, 0, 1, 1)
    heap = [(0, start)]
    dist = {start: 0}
    end = (len(g[0])-1, len(g)-1)
    while len(heap) > 0:
        _, u = heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if u[:2] == end and (not ultra or u[2] > 3):
            end = u
            break
        for v, cost in neighbors(g, u, ultra):
            if v in visited:
                continue
            new_cost = dist[u] + cost
            if v not in dist or new_cost < dist[v]:
                dist[v] = new_cost
                heappush(heap, (new_cost, v))
    return dist[end]

# part 1, takes in lines of file
def p1(file, content, lines):
    global grid
    grid = [list(map(int, list(l))) for l in lines]
    return dijkstra(grid)


# part 2, takes in lines of file
def p2(file, content, lines):
    return dijkstra(grid, True)

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

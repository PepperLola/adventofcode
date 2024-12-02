import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid
sys.setrecursionlimit(1000000000)
# shared variables here
dxyc = [(1, 0, ">"), (-1, 0, "<"), (0, -1, "^"), (0, 1, "v")]
def print_grid(g, visited):
    s = ""
    for y,l in enumerate(g):
        line = ""
        for x,c in enumerate(l):
            if (x, y) in visited:
                line += "O"
            else:
                line += c
        s += line + "\n"
    print(s)

def dfs(visited, g, pt, end, p2=False):
    x, y = pt
    if pt == end:
        print("FOUND END AT", pt)
        return 0
    if pt not in visited:
        possible = []
        # print_grid(g, visited)
        for dx, dy, s in dxyc:
            # print(x+dx, y+dy, len(g[0]), len(g))
            if 0 <= x+dx < len(g[0]) and 0 <= y+dy < len(g):
                new_pt = (x+dx, y+dy)
                if new_pt not in visited and g[new_pt[1]][new_pt[0]] in (".<>^v" if p2 else "." + s):
                    # print(new_pt)
                    new_path = dfs([pt, *visited], g, new_pt, end, p2)
                    # print(new_pt, end, new_path)
                    # print_grid(g, visited)
                    if new_path != -1:
                        possible.append(1+new_path)
        if len(possible) == 0:
            return -1
        # print(possible)
        return max(possible)
    return -1

# part 1, takes in lines of file
def p1(file, content, lines):
    g = [list(line) for line in lines]
    sx = 0
    for x in range(len(g[0])):
        if g[0][x] == ".":
            sx = x
    ex = 0
    for x in range(len(g[0])):
        if g[-1][x] == ".":
            ex = x
    return dfs([], g, (sx, 0), (ex, len(g)-1))

# part 2, takes in lines of file
def p2(file, content, lines):
    g = [list(line) for line in lines]
    sx = 0
    for x in range(len(g[0])):
        if g[0][x] == ".":
            sx = x
    ex = 0
    for x in range(len(g[0])):
        if g[-1][x] == ".":
            ex = x
    vertices = set()
    for y in range(len(g)):
        for x in range(len(g[0])):
            neighbors = 0
            for dx, dy, c in dxyc: 
                if 0 <= x+dx < len(g[0]) and 0 <= y+dy < len(g):
                    neighbors += 1
            if neighbors > 2 and g[y][x] != "#":
                vertices.add((x, y))
    vertices.add((sx, 0))
    vertices.add((ex, len(g)-1))

    edges = {}
    for (vx, vy) in vertices:
        edges[(vx, vy)] = []
        queue = deque([(vx, vy, 0)])
        visited = set()
        while len(queue) > 0:
            x, y, d = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if (x, y) in vertices and (x, y) != (vx, vy):
                edges[(vx, vy)].append(((x, y), d))
                continue
            for dx, dy, c in dxyc:
                if 0 <= x+dx < len(g[0]) and 0 <= y+dy < len(g) and g[y+dy][x+dx] != "#":
                    queue.append((x+dx, y+dy, d+1))

    ans = 0
    SEEN = [[False for _ in range(len(g[0]))] for _ in range(len(g))]
    def dfs2(v, d):
        nonlocal ans
        c,r = v
        if SEEN[r][c]:
            return
        SEEN[r][c] = True
        if r == len(g)-1:
            ans = max(ans, d)
        for (y, yd) in edges[v]:
            dfs2(y,d+yd)
        SEEN[r][c] = False
    dfs2((sx, 0), 0)
    return ans
    # return dfs([], g, (sx, 0), (ex, len(g)-1), True)

filename = "input.txt"

if "test" in sys.argv:
    filename = "test.txt"

with open(filename, "r") as f:
    content = f.read()
    lines = content.splitlines()
    # t = time.perf_counter_ns()
    # a = p1(f, content, lines)
    # dur = time.perf_counter_ns() - t
    #
    # print("\033[0;33m├ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

    t = time.perf_counter_ns()
    a = p2(f, content, lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

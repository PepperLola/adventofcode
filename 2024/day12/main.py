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
import matplotlib.pyplot as plt
import operator
sys.setrecursionlimit(10**6)

# shared variables here
g = []
gr = nx.Graph()

# part 1, takes in lines of file
def p1(file, content, lines):
    global gr, g
    g = letter_grid(lines)
    for y, row in enumerate(g):
        for x, cell in enumerate(row):
            gr.add_node((x, y), val=cell)
            if x > 0 and cell == g[y][x-1]:
                gr.add_edge((x, y), (x-1, y))
            if y > 0 and cell == g[y-1][x]:
                gr.add_edge((x, y), (x, y-1))
    components = list(nx.connected_components(gr))
    ret = 0
    for comp in components:
        perim = 0
        for x, y in comp:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (x+dx, y+dy) not in comp:
                    perim += 1
        ret += perim * len(comp)
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    global gr, g
    components = [gr.subgraph(c) for c in nx.connected_components(gr)]
    ret = 0
    for comp in components:
        sides = 0
        for x, y in comp:
            if (x-1, y) not in comp and (x, y-1) not in comp: sides += 1
            if (x, y-1) not in comp and (x+1, y) not in comp: sides += 1
            if (x+1, y) not in comp and (x, y+1) not in comp: sides += 1
            if (x, y+1) not in comp and (x-1, y) not in comp: sides += 1
            if (x-1, y) in comp and (x, y-1) in comp and (x-1, y-1) not in comp: sides += 1
            if (x, y-1) in comp and (x+1, y) in comp and (x+1, y-1) not in comp: sides += 1
            if (x+1, y) in comp and (x, y+1) in comp and (x+1, y+1) not in comp: sides += 1
            if (x, y+1) in comp and (x-1, y) in comp and (x-1, y+1) not in comp: sides += 1

        ret += sides * len(comp)

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

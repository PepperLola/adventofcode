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
g = []
trailheads = []
ends = []
graph = nx.DiGraph()
global H, W

# part 1, takes in lines of file
def p1(file, content, lines):
    global g, graph, H, W, trailheads, ends
    g = number_grid(lines)

    H = len(g)
    W = len(g[0])

    for r, row in enumerate(g):
        for c, cell in enumerate(row):
            pos = (c, r)
            if cell == 0: trailheads.append(pos)
            if cell == 9: ends.append(pos)
            graph.add_node(pos, label=cell, val=cell)
            if c > 0:
                match cell - g[r][c-1]:
                    case 1: graph.add_edge((c-1, r), pos)
                    case -1: graph.add_edge(pos, (c-1, r))
            if r > 0:
                match cell - g[r-1][c]:
                    case 1: graph.add_edge((c, r-1), pos)
                    case -1: graph.add_edge(pos, (c, r-1))
    ret = 0
    attrs = nx.get_node_attributes(graph, 'val')
    for head in trailheads:
        tree = nx.descendants(graph, head)
        ret += len(list(filter(lambda x: attrs[x] == 9, tree)))
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    global trailheads, ends, graph, g
    ret = 0
    for head in trailheads:
        for end in ends:
            paths = list(nx.all_simple_paths(graph, head, end))
            ret += len(paths)
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

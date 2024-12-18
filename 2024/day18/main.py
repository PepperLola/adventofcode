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
W = 71
to_sim = 1024
bts = set()

# part 1, takes in lines of file
def p1(file, content, lines):
    global W, to_sim, bts
    bts = set(map(lambda x: tuple(map(int, x.split(","))), lines[:to_sim]))
    g = nx.Graph()
    for y in range(W):
        for x in range(W):
            if (x, y) not in bts:
                g.add_node((x, y))
                if x > 0 and (x-1, y) not in bts:
                    g.add_edge((x, y), (x-1, y))
                if y > 0 and (x, y-1) not in bts:
                    g.add_edge((x, y), (x, y-1))

    p = nx.shortest_path(g, (0, 0), (W-1, W-1))

    return len(p) - 1

# part 2, takes in lines of file
def p2(file, content, lines):
    global W, to_sim, bts
    for line in lines[to_sim:]:
        x, y = tuple(map(int, line.split(",")))
        if 0 <= x < W and 0 <= y < W:
            bts.add((x, y))
        g = nx.Graph()
        for y in range(W):
            for x in range(W):
                if (x, y) not in bts:
                    g.add_node((x, y))
                    if x > 0 and (x-1, y) not in bts:
                        g.add_edge((x, y), (x-1, y))
                    if y > 0 and (x, y-1) not in bts:
                        g.add_edge((x, y), (x, y-1))

        try:
            nx.shortest_path(g, (0, 0), (W-1, W-1))
        except:
            return line

filename = "input.txt"

if "test" in sys.argv:
    W = 7
    to_sim = 12
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

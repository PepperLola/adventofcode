import sys
import time
import re
import itertools
from collections import defaultdict, deque, Counter
import math
import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from util import format_time, number_grid

# shared variables here
def distance(j1, j2):
    return math.sqrt((j1[0] - j2[0])**2 + (j1[1] - j2[1])**2 + (j1[2] - j2[2])**2)

g = nx.Graph()

dists = {}
pairs = set()

def find_closest_junctions(pairs):
    global g

    while True:
        pair = pairs[0]
        if pair[1] in g.neighbors(pair[0]):
            pairs.remove(pair)
            pairs.remove((pair[1], pair[0]))
        else:
            return pair

# part 1, takes in lines of file
def p1(file, content, lines):
    global g, pairs
    js = list(map(lambda y: tuple(map(int, y.split(","))), lines))

    # compute distances
    for j1 in js:
        for j2 in js:
            if j1 == j2:
                continue
            if (j1, j2) in dists.keys():
                continue
            dist = distance(j1, j2)
            dists[(j1, j2)] = dist
            dists[(j2, j1)] = dist

    pairs = sorted(dists.keys(), key=lambda x: dists[x], reverse=False)

    for j in js:
        g.add_node(j)

    npr = copy.deepcopy(pairs)

    for _ in range(1000):
        c1, c2 = find_closest_junctions(npr)
        g.add_edge(c1, c2)

    cc = sorted(nx.connected_components(g), key=len, reverse=True)

    return np.prod(list(map(len, cc[:3])))

# part 2, takes in lines of file
def p2(file, content, lines):
    global g, pairs
    c1, c2 = (1,), (-1,)
    i = 0
    npr = copy.deepcopy(pairs)
    while len(list(nx.connected_components(g))) > 1:
        c1, c2 = find_closest_junctions(npr)
        g.add_edge(c1, c2)
        i += 1

    return c1[0] * c2[0]

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

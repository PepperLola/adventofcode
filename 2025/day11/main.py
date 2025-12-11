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
import matplotlib.pyplot as plt
from functools import cache

# shared variables here
g = nx.DiGraph()

# part 1, takes in lines of file
def p1(file, content, lines):
    global g
    for line in lines:
        name, outs = line.split(": ")
        outs = outs.split(" ")
        g.add_node(name)
        for out in outs:
            if not out in g.nodes:
                g.add_node(out)
            g.add_edge(name, out)
    return len(list(nx.all_simple_paths(g, source="you", target="out")))

@cache
def paths(src, fft, dac):
    global g
    dac = dac or src == "dac"
    fft = fft or src == "fft"
    if src == "out":
        return 1 if fft and dac else 0
    return sum([paths(n, fft, dac) for n in g.neighbors(src)])

# part 2, takes in lines of file
def p2(file, content, lines):
    return paths("svr", False, False)

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

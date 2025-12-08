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
g = nx.DiGraph()

# part 1, takes in lines of file
def p1(file, content, lines):
    ret = 0
    W=len(lines[0])
    tracking_cols = set([lines[0].index('S')])
    for line in lines[1:]:
        ns = set()
        for col in tracking_cols:
            if line[col] == "^":
                ret += 1
                ns.add(col+1)
                ns.add(col-1)
            else:
                ns.add(col)
        tracking_cols = ns
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    si = lines[0].find('S')
    npaths = [1 for _ in lines[0]]

    for line in lines[1:][::-1]:
        for x, c in enumerate(line):
            if c == '^':
                npaths[x] = npaths[x-1] + npaths[x+1]

    return npaths[si]

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

import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
from math import lcm
import copy
import numpy as np
from util import format_time, number_grid

# shared variables here
nodes = {}
pat = re.compile(r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)")

# part 1, takes in lines of file
def p1(file, content, lines):
    insts = list(lines[0].strip())
    defs = lines[2:]
    for d in defs:
        match = pat.search(d)
        if not match:
            continue
        nodes[match.group(1)] = (match.group(2), match.group(3))
    curr_node = "AAA"
    i = 0
    for inst in itertools.cycle(insts):
        if curr_node == "ZZZ":
            return i
        if inst == "L":
            curr_node = nodes[curr_node][0]
        elif inst == "R":
            curr_node = nodes[curr_node][1]
        i += 1
    return 0

# part 2, takes in lines of file
def p2(file, content, lines):
    insts = list(lines[0].strip())
    start_nodes = list(filter(lambda n: n.endswith("A"), nodes.keys()))
    ghost_counts = []
    for node in start_nodes:
        i = 0
        for inst in itertools.cycle(insts):
            if node[-1] == "Z":
                ghost_counts.append(i)
                break
            if inst == "L":
                node = nodes[node][0]
            elif inst == "R":
                node = nodes[node][1]
            i += 1
    return lcm(*ghost_counts)

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

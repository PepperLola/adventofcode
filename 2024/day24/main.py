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
from random import randint

# shared variables here
g = nx.DiGraph()
initial_vars = defaultdict()
vars = defaultdict()
wires = defaultdict()

def calc_node_value(node):
    global g, vars, wires
    if node in vars:
        return vars[node]

    for adj in nx.neighbors(g, node):
        vars[adj] = calc_node_value(adj)

    if node in wires:
        return wire_output(node)

    return vars[node]

def wire_output(dest) -> int:
    v1, op, v2 = wires[dest]

    val1, val2 = vars[v1], vars[v2]
    
    if dest in vars:
        return vars[dest]

    val = 0

    if op == "AND":
        val = int(val1 and val2)
    elif op == "OR":
        val = int(val1 or val2)
    elif op == "XOR":
        val = int(val1 != val2)

    return val

def calc():
    for node in g.nodes:
        if node in vars:
            continue

        vars[node] = calc_node_value(node)

# part 1, takes in lines of file
def p1(file, content, lines):
    for line in lines:
        if ":" in line:
            n, v = line.split(": ")
            v = int(v)
            vars[n] = v
            initial_vars[n] = v
            if n not in g:
                g.add_node(n)
        elif line != "":
            s, d = line.split(" -> ")
            s = s.split(" ")
            v1, op, v2 = s
            wires[d] = (v1, op, v2)
            if v1 not in g:
                g.add_node(v1)
            if v2 not in g:
                g.add_node(v2)
            g.add_edge(d, v1, label=op)
            g.add_edge(d, v2, label=op)

    calc()

    ks = sorted([k for k in vars.keys() if k[0] == "z"], reverse=True)
    ret = 0
    for k in ks:
        v = vars[k]
        ret <<= 1
        ret |= v
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    pdot = nx.nx_pydot.to_pydot(g)
    pdot.write_png("graph.png", prog='dot')
    return ",".join(sorted(["z05", "tst", "z11", "sps", "z23", "frt", "pmd", "cgh"]))

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

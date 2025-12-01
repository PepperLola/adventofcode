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

# part 1, takes in lines of file
def p1(file, content, lines):
    c = 50
    n = 0
    for line in lines:
        r, i = line[0], int(line[1:])
        if r == "L":
            c -= i
        else:
            c += i
        if c < 0:
            c += 100
        c %= 100
        if c == 0:
            n += 1
    return n

# part 2, takes in lines of file
def p2(file, content, lines):
    c = 50
    n = 0
    for line in lines:
        r, i = line[0], int(line[1:])
        for k in range(i):
            if r == "L":
                c -= 1
            else:
                c += 1
            if c < 0:
                c += 100
            c %= 100
            if c == 0:
                n += 1
    return n

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

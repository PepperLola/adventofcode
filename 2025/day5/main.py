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
ranges = []

# part 1, takes in lines of file
def p1(file, content, lines):
    global ranges
    ret = 0
    ints = []
    in_ranges = True
    for line in lines:
        if line == "":
            in_ranges = False
            continue
        if in_ranges:
            ranges.append(tuple(map(lambda x: int(x), line.split("-"))))
        else:
            ints.append(int(line))
    ranges.sort()
    for i in ints:
        for n in ranges:
            if n[0] <= i <= n[1]:
                ret += 1
                break
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    global ranges
    idx = 0
    while idx < len(ranges) - 1:
        r1 = ranges[idx]
        r2 = ranges[idx + 1]
        if r1[1] >= r2[0]:
            ranges[idx] = (r1[0], max(r1[1], r2[1]))
            del ranges[idx + 1]
        else:
            idx += 1
    ret = sum([end - start + 1 for start, end in ranges])
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

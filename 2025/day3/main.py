from functools import cache
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
@cache
def max_batt(line: str, digits: int = 2) -> int:
    max_batt = ''
    start = 0
    for i in range(digits):
        m = ''
        for j in range(start, len(line)+i-digits+1):
            v = line[j]
            if v > m:
                m = v
                start = j + 1
        max_batt += m
    return int(max_batt)

# part 1, takes in lines of file
def p1(file, content, lines: list[str]):
    ret = 0
    for line in lines:
        ret += max_batt(line)
    return ret

# part 2, takes in lines of file
def p2(file, content, lines: list[str]):
    ret = 0
    for line in lines:
        ret += max_batt(line, 12)
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

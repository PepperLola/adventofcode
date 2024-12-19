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
from functools import cache

# shared variables here
possible = []
def towel_combs(towel):
    global possible

    @cache
    def calculate(remaining):
        if len(remaining) == 0:
            return 1
        total = 0
        for p in possible:
            if remaining.startswith(p):
                total += calculate(remaining[len(p):])
        return total

    return calculate(towel)

# kept this because it's faster than checking all combinations for part 1
def check_towel(towel):
    global possible
    if len(towel) == 0:
        return True
    for p in possible:
        if towel.startswith(p) and check_towel(towel[len(p):]):
            return True
    return False

# part 1, takes in lines of file
def p1(file, content, lines):
    global possible
    possible = lines[0].split(", ")

    ret = 0
    for line in lines[2:]:
        ret += check_towel(line)
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    global possible

    ret = 0
    for line in lines[2:]:
        ret += towel_combs(line)
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

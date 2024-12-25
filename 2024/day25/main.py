import sys
import time
import re
import itertools
from collections import defaultdict, deque, Counter
import math
import copy
import numpy as np
import networkx as nx
from util import format_time, number_grid, letter_grid

# shared variables here

# part 1, takes in lines of file
def p1(file, content, lines):
    keys = set()
    locks = set()
    for item in content.split("\n\n"):
        g = letter_grid(item.splitlines())
        is_lock = all(c == '#' for c in g[0])
        t = np.transpose(g)
        hts = tuple(map(lambda x: sum(c == '#' for c in x)-1, t))

        if is_lock:
            locks.add(hts)
        else:
            keys.add(hts)

    ret = 0
    for lock in locks:
        for key in keys:
            ret += all(k+l <= 5 for k, l in zip(key, lock))
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    return "Merry Christmas!"

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

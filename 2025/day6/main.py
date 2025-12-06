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
nums = np.array([])
ops = []

# part 1, takes in lines of file
def p1(file, content, lines):
    global nums, ops
    nums = np.array(list(map(lambda x: list(map(int, re.findall(r"\d+", x))), lines[:-1]))).T
    ops = re.findall(r"[^\s]", lines[-1])
    return sum([np.prod(nl) if ops[i] == "*" else np.sum(nl) for i, nl in enumerate(nums)])

# part 2, takes in lines of file
def p2(file, content, lines):
    global ops
    ret = 0
    grid = np.array(letter_grid(lines[:-1])).T
    queue = []
    i = 0
    for nl in grid:
        s = "".join(nl).strip()
        if s == "":
            ret += np.prod(queue) if ops[i] == "*" else np.sum(queue)
            queue.clear()
            i += 1
        else:
            queue.append(int(s))
    ret += np.prod(queue) if ops[i] == "*" else np.sum(queue)
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

import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid

# shared variables here
symbol_posns = []
p = re.compile(r"\d+")

# part 1, takes in lines of file
def p1(file, content, lines):
    total = 0
    for (i, line) in enumerate(lines):
        for (j, c) in enumerate(line):
            if not c in "1234567890.":
                symbol_posns.append([ j, i, c, 1, 0 ])

    for (i, line) in enumerate( lines ):
        match = p.finditer(line)
        for m in match:
            if m is None:
                continue
            start, end = m.span()
            valid = False
            for pos in symbol_posns:
                if i - 1 <= pos[1] <= i + 1 and start - 1 <= pos[0] <= end:
                    valid = True
            if valid:
                total += int(m.group(0))
    return total

# part 2, takes in lines of file
def p2(file, content, lines):
    total = 0
    for (i, line) in enumerate( lines ):
        match = p.finditer(line)
        for m in match:
            if m is None:
                continue
            start, end = m.span()
            for pos in symbol_posns:
                if i - 1 <= pos[1] <= i + 1 and start - 1 <= pos[0] <= end:
                    pos[3] *= int(m.group(0))
                    pos[4] += 1
    for pos in symbol_posns:
        if pos[2] == "*" and pos[4] > 1:
            total += pos[3]
    return total

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

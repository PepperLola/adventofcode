import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
from typing import Deque
import numpy as np
from util import format_time, letter_grid, number_grid

# shared variables here
dirs = [complex(-1, 0), complex(1, 0), complex(0, -1), complex(0, 1)]
steps = 26501365

# part 1, takes in lines of file
def p1(file, content, lines):
    opens = set()
    start = -1
    for y, r in enumerate(lines):
        for x, c in enumerate(r):
            if c == "S":
                start = complex(x, y)
                opens.add(complex(x, y))
            elif c == ".":
                opens.add(complex(x, y))
    posns = {start}
    for _ in range(64):
        posns = {pos+d for pos in posns for d in dirs if pos+d in opens}
    return len(posns)

# part 2, takes in lines of file
def p2(file, content, lines):
    opens = set()
    start = -1
    for y, r in enumerate(lines):
        for x, c in enumerate(r):
            if c == "S":
                start = complex(x, y)
                opens.add(complex(x, y))
            elif c == ".":
                opens.add(complex(x, y))
    t = (steps - 65) // len(lines)
    posns = {start}
    X, Y = [0, 1, 2], [3884, 34564, 95816]
    # for s in range(65 + 131*2 + 1):
    #     if s % 131 == 65:
    #         Y.append(len(posns))
    #     new_posns = set()
    #     for pos in posns:
    #         for d in dirs:
    #             n = pos+d
    #             nw = complex((pos.real+d.real)%131, (pos.imag+d.imag)%131)
    #             if nw in opens:
    #                 new_posns.add(n)
    #     posns = new_posns
    poly = np.polynomial.polynomial.polyfit(X, Y, 2)
    return math.ceil(sum(poly[i]*t**i for i in range(3)))

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

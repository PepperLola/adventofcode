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
from sympy import solve, Eq
from sympy.abc import x, y

# shared variables here
prizes = {}

# part 1, takes in lines of file
def p1(file, content, lines):
    global prizes
    buttons = []
    for line in lines:
        if line == "":
            continue
        nums = tuple(map(int, re.findall(r"\d+", line)))
        if "Button" in line:
            buttons.append(nums)
        elif "Prize" in line:
            nx, ny = nums
            nums = (nx, ny)
            prizes[nums] = buttons
            buttons = []
    ret = 0
    for prize, buttons in prizes.items():
        eq1 = Eq(buttons[0][0] * x + buttons[1][0] * y, prize[0])
        eq2 = Eq(buttons[0][1] * x + buttons[1][1] * y, prize[1])
        res = solve([eq1, eq2], [x, y])
        if int(res[x]) == res[x] and int(res[y]) == res[y]:
            ret += 3*res[x] + res[y]
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    global prizes
    ret = 0
    for prize, buttons in prizes.items():
        eq1 = Eq(buttons[0][0] * x + buttons[1][0] * y, prize[0] + 10000000000000)
        eq2 = Eq(buttons[0][1] * x + buttons[1][1] * y, prize[1] + 10000000000000)
        res = solve([eq1, eq2], [x, y])
        if int(res[x]) == res[x] and int(res[y]) == res[y]:
            ret += 3*res[x] + res[y]
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

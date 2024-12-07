import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
import networkx as nx
from util import format_time, number_grid

# shared variables here
ADD = 0
MUL = 1
CON = 2
def test(nums, comb):
    ret = nums[0]
    oi = 0
    for n in nums[1:]:
        op = comb[oi]
        if op == ADD:
            ret += n
        elif op == MUL:
            ret *= n
        elif op == CON:
            ret = int(str(ret) + str(n))
        oi += 1
    return ret

# part 1, takes in lines of file
def p1(file, content, lines):
    ret = 0
    o = [ADD, MUL]
    for line in lines:
        nums = list(map(int, re.findall("\\d+", line)))
        res = nums[0]
        nums = nums[1:]
        combs = itertools.product(o, repeat=len(nums)-1)
        for comb in combs:
            # print("COMB: {0:b}".format(comb))
            t = test(nums, comb)
            if t == res:
                ret += res
                break
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    ret = 0
    o = [ADD, MUL, CON]
    for line in lines:
        nums = list(map(int, re.findall("\\d+", line)))
        res = nums[0]
        nums = nums[1:]
        combs = itertools.product(o, repeat=len(nums)-1)
        for comb in combs:
            t = test(nums, comb)
            if t == res:
                ret += res
                break
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

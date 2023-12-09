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
def find_diffs(nums):
    diffs = []
    for i in range(len(nums)-1):
        diffs.append(nums[i+1]-nums[i])
    return diffs

# part 1, takes in lines of file
def p1(file, content, lines):
    total = 0

    for line in lines:
        nums = list(map(int, line.split(" ")))
        diffs = [nums]
        while not all(map(lambda x: x == 0, diffs[-1])):
            diffs.append(find_diffs(diffs[-1]))
        diffs = diffs[:-1]
        diffs.reverse()
        diffs[0].append(diffs[0][0]) # all const
        for i in range(1, len(diffs)):
            diffs[i].append(diffs[i][-1]+diffs[i-1][-1])
        total += diffs[-1][-1]
    return total

# part 2, takes in lines of file
def p2(file, content, lines):
    total = 0

    for line in lines:
        nums = list(map(int, line.split(" ")))
        diffs = [nums]
        while not all(map(lambda x: x == 0, diffs[-1])):
            diffs.append(find_diffs(diffs[-1]))
        diffs = diffs[:-1]
        diffs.reverse()
        diffs[0].append(diffs[0][0])
        for i in range(1, len(diffs)):
            diffs[i] = [(diffs[i][0]-diffs[i-1][0])] + diffs[i]
        total += diffs[-1][0]
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

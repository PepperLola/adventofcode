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

# part 1, takes in lines of file
def p1(file, content, lines):
    su = 0
    for line in lines:
        nums = re.findall(r"\d", line)
        if len(nums) > 0:
            su += int(nums[0] + nums[-1])
    return su

# part 2, takes in lines of file
def p2(file, content, lines):
    names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    su = 0
    for line in lines:
        for i, name in enumerate(names):
            line = line.replace(name, name[0] + str(i + 1) + name[-1]) # add first and last back so overlapping names works
        nums = re.findall(r"\d", line)
        if len(nums) > 0:
            su += int(nums[0] + nums[-1])
    return su

filename = "input.txt"

if "test" in sys.argv:
    filename = "test.txt"

with open(filename, "r") as f:
    file = f.read()
    lines = file.splitlines()
    t = time.perf_counter_ns()
    a = p1(f, file, lines)
    dur = time.perf_counter_ns() - t

    print("\033[0;33m├ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

    t = time.perf_counter_ns()
    a = p2(f, file, lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

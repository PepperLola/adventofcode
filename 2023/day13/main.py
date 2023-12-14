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
def check_horizontal_reflect(pattern, y):
    non_symmetrical = 0
    for row in range(len(pattern)):
        up = y-row
        down = y+1+row
        if 0 <= up < down < len(pattern):
            for i in range(len(pattern[0])):
                if pattern[up][i] != pattern[down][i]:
                    non_symmetrical += 1
    return non_symmetrical

def check_vertical_reflect(pattern, x):
    non_symmetrical = 0
    for col in range(len(pattern[0])):
        left = x-col
        right = x+1+col
        if 0 <= left < right < len(pattern[0]):
            for i in range(len(pattern)):
                if pattern[i][left] != pattern[i][right]:
                    non_symmetrical += 1
    return non_symmetrical

# part 1, takes in lines of file
def p1(file, content, lines):
    patterns = []
    temp_pattern = []
    for line in lines:
        if line.strip() == "":
            patterns.append(temp_pattern)
            temp_pattern = []
        else:
            temp_pattern.append(line.strip())
    patterns.append(temp_pattern)
    total = 0
    for pattern in patterns:
        for y in range(len(pattern)-1):
            if check_horizontal_reflect(pattern, y) == 0:
                total += 100*(y+1)
        for x in range(len(pattern[0])-1):
            if check_vertical_reflect(pattern, x) == 0:
                total += x+1
    return total

# part 2, takes in lines of file
def p2(file, content, lines):
    patterns = []
    temp_pattern = []
    for line in lines:
        if line.strip() == "":
            patterns.append(temp_pattern)
            temp_pattern = []
        else:
            temp_pattern.append(line.strip())
    patterns.append(temp_pattern)
    total = 0
    for pattern in patterns:
        for y in range(len(pattern)-1):
            non_symmetrical = check_horizontal_reflect(pattern, y)
            if non_symmetrical == 1:
                total += 100*(y+1)
        for x in range(len(pattern[0])-1):
            non_symmetrical = check_vertical_reflect(pattern, x)
            if non_symmetrical == 1:
                total += x+1
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

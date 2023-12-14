import sys
import time
import re
import itertools
from functools import lru_cache
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid

# shared variables here
def check_arrangement(line, counts):
    # print(line)
    line_sub = list(filter(lambda x: x != "", re.sub(f" +", " ", line.replace(".", " ")).split(" ")))
    # print(line_sub)
    line_lens = [len(l) for l in line_sub]
    # print(line_lens, counts)
    # print(line_lens == counts)
    # input()
    return line_lens == counts

# part 1, takes in lines of file
CACHE = {}

def solve(row, counts, i, i2, curr_len):
    val = (i, i2, curr_len)
    if val in CACHE:
        return CACHE[val]
    if i == len(row):
        if i2 == len(counts) and curr_len == 0:
            return 1
        elif i2 == len(counts)-1 and counts[i2] == curr_len:
            return 1
        else:
            return 0
    total = 0
    for c in ['.', '#']:
        if row[i] == c or row[i] == '?':
            if c == '.' and curr_len == 0:
                total += solve(row, counts, i+1, i2, 0)
            elif c == '.' and curr_len > 0 and i2 < len(counts) and counts[i2] == curr_len:
                total += solve(row, counts, i+1, i2+1, 0)
            elif c == "#":
                total += solve(row, counts, i+1, i2, curr_len+1)


    CACHE[val] = total
    return total

def p1(file, content, lines):
    total = 0
    for line in lines:
        CACHE.clear()
        split = line.split(" ")
        counts = list(map(int, split[1].split(",")))
        total += solve(split[0], counts, 0, 0, 0)
    return total

# part 2, takes in lines of file
def p2(file, content, lines):
    total = 0
    for line in lines:
        CACHE.clear()
        split = line.split(" ")
        row = "?".join([split[0]] * 5)
        counts = list(map(int, (",".join(split[1].split(",") * 5).split(","))))
        total += solve(row, counts, 0, 0, 0)
            
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

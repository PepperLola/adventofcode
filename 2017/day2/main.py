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
    ret = 0
    for line in lines:
        arr = list(map(int, line.split("\t")))
        s = sorted(arr)
        ret += abs(s[0] - s[-1])
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    ret = 0
    for line in lines:
        arr = list(map(int, line.split("\t")))
        for i in range(len(arr)):
            v1 = arr[i]
            done = False
            for j in arr[i+1:]:
                if v1 % j == 0 or j % v1 == 0:
                    done = True
                    ret += max(v1, j) // min(v1, j)
                    break
            if done:
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

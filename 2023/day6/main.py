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

def ways_to_win(time, distance):
    # quadform with ineq `distance < x*(time-x)`
    sq = math.sqrt(time**2-4*distance)
    quad1 = (time+sq)/-2
    quad2 = (time-sq)/-2

    return math.ceil(quad2)-math.floor(quad1)-1

# part 1, takes in lines of file
def p1(file, content, lines):
    times = list(map(int, re.sub(r" +", " ", lines[0][5:].strip()).split()))
    distances = list(map(int, re.sub(r" +", " ", lines[1][9:].strip()).split()))
    matches = zip(times, distances)
    total = 1
    for match in matches:
        ways = ways_to_win(match[0], match[1])
        total *= ways
    return total

# part 2, takes in lines of file
def p2(file, content, lines):
    time = int(re.sub(r" +", "", lines[0][5:].strip()))
    distance = int(re.sub(r" +", "", lines[1][9:].strip()))
    return ways_to_win(time, distance)

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

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
row_no_galaxy = []
col_no_galaxy = []
original_points = []

def scale(points, times=2):
    global row_no_galaxy, col_no_galaxy
    for point in points:
        diff = 0
        for col in col_no_galaxy:
            if point[0] > col:
                diff += times-1
        point[0] += diff
        diff = 0
        for row in row_no_galaxy:
            if point[1] > row:
                diff += times-1
        point[1] += diff

def sum_distances(points):
    return sum(itertools.starmap(lambda x, y: abs(y[0]-x[0]) + abs(y[1]-x[1]), itertools.combinations(points, 2)))

# part 1, takes in lines of file
def p1(file, content, lines):
    global original_points, row_no_galaxy, col_no_galaxy
    for (y, line) in enumerate(lines):
        has_galaxy = False
        for (x, c) in enumerate(line):
            if c == "#":
                original_points.append([ x, y ])
                has_galaxy = True
        if not has_galaxy:
            row_no_galaxy.append(y)

    points = copy.deepcopy(original_points)

    for x in range(len(lines[0])):
        if len([point[0] for point in points if point[0] == x]) == 0:
            col_no_galaxy.append(x)

    scale(points)
    return sum_distances(points)

# part 2, takes in lines of file
def p2(file, content, lines):
    scale(original_points, times=1000000)

    return sum_distances(original_points)

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

import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid
from shapely.geometry.polygon import Polygon
import matplotlib.pyplot as plt

# shared variables here
m = {"R":(1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}

# part 1, takes in lines of file
def p1(file, content, lines):
    x, y = 0, 0
    pts = []
    perim = 1
    for line in lines:
        dir, n, col = line.split(" ")
        dx, dy = m[dir]
        n = int(n)
        perim += n
        col = col[1:-2]
        pts.append((x+dx*n, y+dy*n))
        x += dx*n
        y += dy*n
    poly = Polygon(pts)
    return int(poly.area + math.ceil(perim/2))
        
# part 2, takes in lines of file
def p2(file, content, lines):
    x, y = 0, 0
    pts = []
    perim = 1
    for line in lines:
        _, _, col = line.split(" ")
        col = col[2:-1]
        dir_n = col[-1]
        n = int(col[:-1], 16)
        dir = {"0":"R","1":"D","2":"L","3":"U"}[dir_n]
        dx, dy = m[dir]

        perim += n
        pts.append((x+dx*n, y+dy*n))
        x += dx*n
        y += dy*n
    poly = Polygon(pts)
    return int(poly.area + math.ceil(perim/2))

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

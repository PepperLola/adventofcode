import sys
import time
import re
import itertools
from collections import defaultdict, deque, Counter
import math
import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from shapely.geometry import Polygon
from shapely.prepared import prep
from util import format_time, number_grid

# shared variables here
pts = []
combos = []

# part 1, takes in lines of file
def p1(file, content, lines):
    global pts, combos
    pts = [(int(x), int(y)) for x, y in map(lambda x: x.split(","), lines)]

    combos = list(itertools.combinations_with_replacement(pts, 2))

    return max([(abs(x2 - x1)+1) * (abs(y2 - y1)+1) for (x1, y1), (x2, y2) in combos])

# part 2, takes in lines of file
def p2(file, content, lines):
    global pts, combos

    a = 0
    polygon = Polygon(pts)
    prepared = prep(polygon)

    for (x1, y1), (x2, y2) in combos:
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)

        rect = Polygon([
            (min_x, min_y),
            (max_x, min_y),
            (max_x, max_y),
            (min_x, max_y)
        ])

        if not prepared.covers(rect):
            continue
        a = max(a, (max_x - min_x + 1) * (max_y - min_y + 1))

    return a

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

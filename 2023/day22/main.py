import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid
from shapely import intersects, LineString

# shared variables here
def fall(bricks) -> tuple[bool, list[list[tuple[int, int, int]]]]:
    new_bricks = []
    modified = 0
    points = set()
    for bs, be in bricks:
        sx, sy, sz = bs
        ex, ey, ez = be
        for x in range(sx, ex+1):
            for y in range(sy, ey+1):
                points.add((x, y, ez))
    for brick in bricks:
        supported = False
        (sx, sy, sz), (ex, ey, ez) = brick
        for x in range(sx, ex+1):
            for y in range(sy, ey+1):
                if sz == 1 or (x, y, sz - 1) in points:
                    supported = True
                    break
            if supported:
                break
        if supported:
            new_bricks.append(brick)
            continue
        modified += 1
        new_bricks.append([(sx, sy, sz-1), (ex, ey, ez-1)])
    return modified > 0, new_bricks

bricks = []

# part 1, takes in lines of file
def p1(file, content, lines):
    global bricks
    for line in lines:
        start, end = map(lambda x: tuple(map(int, x.split(","))), line.split("~"))
        bricks.append([ start, end ])

    fell = True
    while fell: fell, bricks = fall(bricks)

    total = 0
    before = bricks.copy()
    for i in range(len(before)):
        after = before[:i] + before[i+1:]
        fell, _ = fall(after)
        if not fell:
            total += 1
    return total

# part 2, takes in lines of file
def p2(file, content, lines):
    global bricks

    total = 0
    for i in range(len(bricks)):
        before = bricks.copy()
        del before[i]
        after = before.copy()
        fell = True
        while fell:
            fell, after = fall(after)
        fallen = 0
        for a,b in zip(before, after):
            if a != b:
                fallen += 1
        total += fallen 
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

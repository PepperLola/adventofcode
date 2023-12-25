import sys
import time
import re
import itertools
from itertools import combinations
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid
import z3

# shared variables here
stones = []

def intersection(b1, b2):
    p1, v1, p2, v2 = [np.array(p[:2]) for p in [*b1, *b2]]
    a = np.array([v1, -v2]).T
    if np.linalg.det(a) == 0:
        return None
    b = p2 - p1
    t = np.linalg.solve(a, b)
    if np.any(t < 0):
        return None
    return p1 + t[0] * v1

# part 1, takes in lines of file
def p1(file, content, lines):
    global stones
    for line in lines:
        pos, vel = line.split(" @ ")
        x, y, z = list(map(int, pos.split(", ")))
        vx, vy, vz = list(map(int, vel.split(", ")))
        stones.append([(x, y, z), (vx, vy, vz)])
    total = 0
    for p1, p2 in itertools.combinations(stones, 2):
        point = intersection(p1, p2)
        if point is not None and np.all(200000000000000 <= point) and np.all(point <= 400000000000000):
            total += 1
    return total

# part 2, takes in lines of file
def p2(file, content, lines):
    global stones
    solver = z3.Solver()
    x, y, z, vx, vy, vz = [z3.Int(p) for p in ["x", "y", "z", "vx", "vy", "vz"]]
    t = z3.IntVector("t", len(stones))

    for i in range(3):
        (sx, sy, sz), (svx, svy, svz) = stones[i]
        solver.add([sx + svx * t[i] == x + vx * t[i]])
        solver.add([sy + svy * t[i] == y + vy * t[i]])
        solver.add([sz + svz * t[i] == z + vz * t[i]])

    if solver.check() == z3.sat:
        model = solver.model()
        return sum([model.eval(p).as_long() for p in [x,y,z]])

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

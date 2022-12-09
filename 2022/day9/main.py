import sys
import time
import re
import math
import itertools
import numpy as np

# shared variables here
dxm = {"L": -1, "U": 0, "R": 1, "D": 0} #direction x map
dym = {"L": 0, "U": 1, "R": 0, "D": -1}

def format_board(knots):
    grid = np.tile(-1, (50, 100))
    for i in range(len(knots)):
        knot = knots[i]
        grid[-knots[i][1] + 25, knots[i][0] + 50] = i

    s = ""
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            s += str(int(grid[y][x])) if grid[y][x] > -1 else "."
        s += "\n"
    return s

# part 1, takes in lines of file
def p1(lines):
    hx, hy, tx, ty = 0, 0, 0, 0
    visited = set()
    for line in lines:
        line = line.strip()
        d = line[0]
        amt = int(line[2:])
        
        for i in range(amt):
            if d == "L":
                hx -= 1
                if abs(hx - tx) > 1:
                    tx -= 1
                    if hy != ty:
                        ty += (hy - ty)
            if d == "R":
                hx += 1
                if abs(hx - tx) > 1:
                    tx += 1
                    if hy != ty:
                        ty += (hy - ty)
            if d == "U":
                hy += 1
                if abs(hy - ty) > 1:
                    ty += 1
                    if hx != tx:
                        tx += (hx - tx)
            if d == "D":
                hy -= 1
                if abs(hy - ty) > 1:
                    ty -= 1
                    if hx != tx:
                        tx += (hx - tx)
            visited.add((tx, ty))
    return len(visited)

def move_knot(prev, curr):
    dx = prev[0] - curr[0]
    dy = prev[1] - curr[1]
    
    if abs(dx) <= 1 and abs(dy) <= 1:
        pass
    elif abs(dx) >= 2 and abs(dy) >= 2:
        curr = [prev[0] - np.sign(dx), prev[1] - np.sign(dy)]
    elif abs(dx) >= 2:
        curr = [prev[0] - np.sign(dx), prev[1]]
    elif abs(dy) >= 2:
        curr = [prev[0], prev[1] - np.sign(dy)]
    return curr

# part 2, takes in lines of file
def p2(lines):
    knots = [[0, 0] for i in range(10)]
    visited = set()
    for line in lines:
        line = line.strip()
        d = line[0]
        amt = int(line[2:])

        dx, dy = dxm[d], dym[d]
        for i in range(amt):
            knots[0] = [knots[0][0] + dx, knots[0][1] + dy]
            knots[1] = move_knot(knots[0], knots[1])

            for i in range(2, len(knots)):
                knots[i] = move_knot(knots[i - 1], knots[i])
            visited.add(tuple(knots[9]))
    return len(visited)

filename = "input.txt"

if "test" in sys.argv:
    filename = "test.txt"

def format_time(time_ns):
    names = ["hr", "m", "s", "ms", "µs", "ns"]
    names.reverse()
    times = [
        time_ns % 1000,
        (time_ns // 1000) % 1000,
        (time_ns // (1000 * 10**3)) % 1000,
        (time_ns // (1000 * 10**6)) % 60,
        (time_ns // (1000 * 10**6) // 60) % 60,
        (time_ns // (1000 * 10**6) // 60 // 60) % 60
    ]
    for i in range(0, len(times)):
        if i < len(times) - 1:
            if times[i + 1] == 0:
                return "%s%s " % (times[i], names[i])
        else:
            return "%s%s " % (times[i], names[i])

with open(filename, "r") as f:
    lines = f.readlines()
    t = time.perf_counter_ns()
    a = p1(lines)
    dur = time.perf_counter_ns() - t

    print("\033[0;33m├ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

    t = time.perf_counter_ns()
    a = p2(lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

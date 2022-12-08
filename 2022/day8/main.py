import sys
import time
import re
import itertools
import copy
import numpy as np

# shared variables here
def is_visible_from(grid, x, y, dx, dy, height = 0):
    is_visible = True
    if height == 0:
        height = grid[y][x]
    if dx != 0:
        if 0 <= x + dx < len(grid[0]):
            return grid[y][x + dx] < height and is_visible_from(grid, x + dx, y, dx, dy, height)
        else:
            return True
    elif dy != 0:
        if 0 <= y + dy < len(grid):
            return grid[y + dy][x] < height and is_visible_from(grid, x, y + dy, dx, dy, height)
        else:
            return True
    else:
        return False

def view_distance(grid, x, y, dx, dy, height = 0):
    if height == 0:
        height = grid[y][x]
    if dx != 0:
        if 0 <= x + dx < len(grid[0]):
            if grid[y][x + dx] < height:
                return 1 + view_distance(grid, x + dx, y, dx, dy, height)
            else:
                return 1
        else:
            return 0
    elif dy != 0:
        if 0 <= y + dy < len(grid[0]):
            if grid[y + dy][x] < height:
                return 1 + view_distance(grid, x, y + dy, dx, dy, height)
            else:
                return 1
        else:
            return 0
    else:
        return 0

# part 1, takes in lines of file
def p1(lines):
    w = len(lines[0].strip())
    h = len(lines)
    grid = np.zeros((w, h))
    for y in range(len(lines)):
        for x in range(len(lines[0].strip())):
            grid[y][x] = lines[y][x]

    visible = w * 2 + (h - 2) * 2
    visible = 0
    visible_grid = copy.deepcopy(grid)

    for y in range(h):
        for x in range(w):
            left = is_visible_from(grid, x, y, -1, 0)
            right = is_visible_from(grid, x, y, 1, 0)
            top = is_visible_from(grid, x, y, 0, -1)
            bottom = is_visible_from(grid, x, y, 0, 1)
            if left or right or top or bottom:
                visible += 1
                visible_grid[y][x] = 1
            else:
                visible_grid[y][x] = 0

    return visible

# part 2, takes in lines of file
def p2(lines):
    w = len(lines[0].strip())
    h = len(lines)
    grid = np.zeros((w, h))
    for y in range(len(lines)):
        for x in range(len(lines[0].strip())):
            grid[y][x] = lines[y][x]

    scores = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            scores.append(
                view_distance(grid, x, y, 1, 0) *
                view_distance(grid, x, y, -1, 0) *
                view_distance(grid, x, y, 0, 1) *
                view_distance(grid, x, y, 0, -1)
            )

    scores.sort(reverse=True)
    return scores[0]

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

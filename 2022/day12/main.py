import sys
import time
import re
import itertools
from collections import deque
import numpy as np

# shared variables here
alphabet = "abcdefghijklmnopqrstuvwxyz"
def parse_elevations(lines):
    e = np.zeros((len(lines), len(lines[0].strip())))
    S = (0, 0)
    E = (0, 0)
    for y in range(len(lines)):
        for x in range(len(lines[0].strip())):
            c = lines[y].strip()[x]
            if c == "S":
                e[y][x] = 0
                S = (x, y)
            elif c == "E":
                e[y][x] = 25
                E = (x, y)
            else:
                e[y][x] = alphabet.index(lines[y][x])
    return (e, S, E)

# part 1, takes in lines of file
def p1(lines):
    elevations, start, end = parse_elevations(lines)

    Q = deque()
    Q.append((start, 0))

    visited = set()
    while Q:
        (x, y), dist = Q.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if (x, y) == end:
            return dist
        if x > 0 and elevations[y][x - 1] - elevations[y][x] <= 1:
            Q.append(((x - 1, y), dist + 1))
        if x < len(elevations[0]) - 1 and elevations[y][x + 1] - elevations[y][x] <= 1:
            Q.append(((x + 1, y), dist + 1))
        if y > 0 and elevations[y - 1][x] - elevations[y][x] <= 1:
            Q.append(((x, y - 1), dist + 1))
        if y < len(elevations) - 1 and elevations[y + 1][x] - elevations[y][x] <= 1:
            Q.append(((x, y + 1), dist + 1))
            

# part 2, takes in lines of file
def p2(lines):
    elevations, start, end = parse_elevations(lines)

    Q = deque()
    for y in range(len(elevations)):
        for x in range(len(elevations[y])):
            if elevations[y][x] == 0:
                Q.append(((x, y), 0))

    visited = set()
    while Q:
        (x, y), dist = Q.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if (x, y) == end:
            return dist
        if x > 0 and elevations[y][x - 1] - elevations[y][x] <= 1:
            Q.append(((x - 1, y), dist + 1))
        if x < len(elevations[0]) - 1 and elevations[y][x + 1] - elevations[y][x] <= 1:
            Q.append(((x + 1, y), dist + 1))
        if y > 0 and elevations[y - 1][x] - elevations[y][x] <= 1:
            Q.append(((x, y - 1), dist + 1))
        if y < len(elevations) - 1 and elevations[y + 1][x] - elevations[y][x] <= 1:
            Q.append(((x, y + 1), dist + 1))

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

import sys
import time
import re
import itertools
import numpy as np

# shared variables here

# part 1, takes in lines of file
def p1(lines):
    x, y = 0, 0
    d = 0 # 0 = NORTH; 1 = WEST; 2 = SOUTH; 3 = EAST
    line = lines[0].strip()
    for step in line.split(", "):
        if "L" in step:
            d += 1
        elif "R" in step:
            d -= 1

        d = (d + 4) % 4

        steps = int(step[1:])
        if d == 0:
            y -= steps
        elif d == 1:
            x -= steps
        elif d == 2:
            y += steps
        elif d == 3:
            x += steps

    return x+y

# part 2, takes in lines of file
def p2(lines):
    x, y = 0, 0
    visited = set()
    d = 0 # 0 = NORTH; 1 = WEST; 2 = SOUTH; 3 = EAST
    line = lines[0].strip()
    for step in line.split(", "):
        if "L" in step:
            d = (d + 1) % 4
        elif "R" in step:
            d = (d - 1) % 4


        steps = int(step[1:])
        for i in range(steps):
            if d == 0:
                y -= 1
            elif d == 1:
                x -= 1
            elif d == 2:
                y += 1
            elif d == 3:
                x += 1

            if (x, y) in visited:
                return x+y
            else:
                visited.add((x, y))

    return x+y

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

import sys
import time
import re
import itertools
import numpy as np

# shared variables here
WIDTH = 3
HEIGHT = 3

def get_value(x, y):
    return WIDTH * y + x + 1

# part 1, takes in lines of file
def p1(lines):
    code = ""
    x, y = 1, 1
    for line in lines:
        line = line.strip()
        for c in line:
            if c == "U":
                if y > 0:
                    y -= 1
            elif c == "D":
                if y < HEIGHT - 1:
                    y += 1
            elif c == "L":
                if x > 0:
                    x -= 1
            elif c == "R":
                if x < WIDTH - 1:
                    x += 1
        code += str(get_value(x, y))
    return code

keypad = [
[-1,  -1,   1,  -1, -1],
[-1,   2,   3,   4, -1],
[ 5,   6,   7,   8,  9],
[-1, "A", "B", "C", -1],
[-1,  -1, "D",  -1, -1]
]

# part 2, takes in lines of file
def p2(lines):
    WIDTH = 5
    HEIGHT = 5
    code = ""
    x, y = 0, 2
    for line in lines:
        line = line.strip()
        for c in line:
            if c == "U":
                if y > 0 and keypad[y - 1][x] != -1:
                    y -= 1
            elif c == "D":
                if y < HEIGHT - 1 and keypad[y + 1][x] != -1:
                    y += 1
            elif c == "L":
                if x > 0 and keypad[y][x - 1] != -1:
                    x -= 1
            elif c == "R":
                if x < WIDTH - 1 and keypad[y][x + 1] != -1:
                    x += 1
        code += str(keypad[y][x])
    return code

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

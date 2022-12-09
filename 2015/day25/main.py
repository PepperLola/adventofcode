import sys
import time
import re
import itertools
import numpy as np

# shared variables here
row = 2978
col = 3083

def get_index(r, c):
    return int(((c+r+1)*(c+r+2))/2-r)

def get_value(idx):
    # return 20151125*(252533**idx) % 33554393
    val = 20151125
    for i in range(idx-1):
        val *= 252533
        val %= 33554393
    return val

# part 1, takes in lines of file
def p1(lines):
    # for r in range(6):
        # for c in range(6):
            # print(get_value(get_index(r, c)), end=" | ")
        # print("\n")
    idx = get_index(row - 1, col - 1)
    # print(idx)
    return get_value(idx)

# part 2, takes in lines of file
def p2(lines):
    return 0

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

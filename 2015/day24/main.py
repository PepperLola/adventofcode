import sys
import time
import re
import itertools
import numpy as np

# shared variables here

# part 1, takes in lines of file
def p1(lines):
    weights = []
    for line in lines:
        weights.append(int(line.strip()))

    
    weights.sort(reverse=True)
    target = sum(weights) / 3
    shortest_length = 1000
    groups = []
    found_all = False
    for i in range(len(weights) // 2):
        if found_all:
            break
        combs = itertools.combinations(weights, i)
        for comb in combs:
            if sum(comb) == target:
                if len(comb) > shortest_length:
                    found_all = True
                    break
                else:
                    groups.append(comb)
                    shortest_length = len(comb)

    groups.sort(key=lambda x: np.prod(x))

    return np.prod(groups[0])

# part 2, takes in lines of file
def p2(lines):
    weights = []
    for line in lines:
        weights.append(int(line.strip()))

    
    weights.sort(reverse=True)
    target = sum(weights) / 4
    shortest_length = 1000
    groups = []
    found_all = False
    for i in range(len(weights) // 2):
        if found_all:
            break
        combs = itertools.combinations(weights, i)
        for comb in combs:
            if sum(comb) == target:
                if len(comb) > shortest_length:
                    found_all = True
                    break
                else:
                    groups.append(comb)
                    shortest_length = len(comb)

    groups.sort(key=lambda x: np.prod(x))

    return np.prod(groups[0])

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

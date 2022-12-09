import sys
import time
import re
import itertools
import numpy as np
from collections import defaultdict

# shared variables here
cols = []

# part 1, takes in lines of file
def p1(lines):
    cols = [[] for i in range(len(lines[0].strip()))]
    for k in range(len(lines[0].strip())):
        for i in range(len(lines)):
            cols[k].append(lines[i][k].strip())

    message = ""
    for k in range(len(lines[0].strip())):
        freqs = {}
        for c in cols[k]:
            if c in freqs:
                freqs[c] += 1
            else:
                freqs[c] = 1
        s = sorted(list(freqs.keys()), key=lambda x: freqs[x], reverse=True)
        message += s[0]
    return message

# part 2, takes in lines of file
def p2(lines):
    cols = [[] for i in range(len(lines[0].strip()))]
    for k in range(len(lines[0].strip())):
        for i in range(len(lines)):
            cols[k].append(lines[i][k].strip())

    message = ""
    for k in range(len(lines[0].strip())):
        freqs = {}
        for c in cols[k]:
            if c in freqs:
                freqs[c] += 1
            else:
                freqs[c] = 1
        s = sorted(list(freqs.keys()), key=lambda x: freqs[x])
        message += s[0]
    return message

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

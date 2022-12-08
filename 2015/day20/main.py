import sys
import time
import re
import itertools
import numpy as np
import math

# shared variables here
def divisors(num):
    if num == 1:
        return [1]
    res = [1, num]
    max_to_check = int(math.sqrt(num)) + 1
    for i in range(2, max_to_check):
        if num % i == 0:
            res += [i, num / i]
    return res


# part 1, takes in lines of file
def p1(lines):
    line = lines[0].strip()
    inp = int(int(line) / 10)
    i = 200000
    while True:
        if sum(divisors(i)) >= inp:
            return i
        i += 1
    return 0

# part 2, takes in lines of file
def p2(lines):
    line = lines[0].strip()
    inp = int(int(line) / 11)
    i = 200000
    while True:
        if sum([k for k in divisors(i) if i / k <= 50]) >= inp:
            return i
        i += 1
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

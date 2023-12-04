import sys
import time
import re
import itertools
import numpy as np

# shared variables here

# part 1, takes in lines of file
def p1(lines):
    size = 0
    for file in lines:
        file = file.strip()
        in_marker = False
        times = 1
        i = 0
        while i < len(file):
            c = file[i]
            if c == "(" and not in_marker:
                closing = file.index(")", i)
                marker = file[i+1:closing]
                s = marker.split("x")
                amt = int(s[0])
                times = int(s[1])
                i += amt + closing - i + 1
                size += amt * times
                continue
            i += 1
            size += 1
                
    return size

def decompress(s, depth = 0):
    matched = False
    while True:
        match = re.search(r"\((\d+)x(\d+)\)", s)
        if not match:
            break
        matched = True
        start, end = match.span()
        num_chars = int(match.group(1))
        span = s[end:end+num_chars]
        times = int(match.group(2))
        s = s[:start] + span*times + s[end+num_chars:]
    if not matched:
        return s
    return decompress(s, depth+1)

def find_length(s, n=1):
    matched = False
    length = 0
    while True:
        match = re.search(r"\((\d+)x(\d+)\)", s)
        if not match:
            break
        start, end = match.span()
        length += len(s[:start])
        num_chars = int(match.group(1))
        times = int(match.group(2))
        matched = True
        sub = s[end:end+num_chars]
        length += find_length(sub, times)
        s = s[end+num_chars:]
    if not matched:
        return len(s)*n
    else:
        return length*n

# part 2, takes in lines of file
def p2(lines):
    return find_length(lines[0])

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

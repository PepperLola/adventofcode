import sys
import time
import re
import itertools
import hashlib
import numpy as np

# shared variables here

# part 1, takes in lines of file
def p1(lines):
    door_id = "wtnhxymk"
    counter = 0
    code = ""
    while len(code) < 8:
        print("Found " + str(len(code)) + "/8", end="\r")
        h = hashlib.md5((door_id + str(counter)).encode('utf-8')).hexdigest()
        if h[:5] == "00000":
            code += h[5]
        counter += 1

    return code

# part 2, takes in lines of file
def p2(lines):
    door_id = "wtnhxymk"
    counter = 0
    code = [""] * 8
    filled = 0
    while filled < 8:
        print("Found " + str(filled) + "/8", end="\r")
        h = hashlib.md5((door_id + str(counter)).encode('utf-8')).hexdigest()
        if h[:5] == "00000" and h[5].isnumeric():
            idx = int(h[5])
            if idx < 8 and code[idx] == "":
                filled += 1
                code[int(h[5])] = h[6]
        counter += 1
    return "".join(code)


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

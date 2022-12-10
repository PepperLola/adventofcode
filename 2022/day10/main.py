import sys
import time
import re
import itertools
import numpy as np

# shared variables here
def get_state_at_cycle(lines, target):
    X = 1
    cycle = 0
    for line in lines:
        line = line.strip()
        if "addx" in line:
            s = line.split(" ")
            n = int(s[1])
            cycle += 1
            if cycle >= target:
                return X * cycle
            cycle += 1
            if cycle >= target:
                return X * cycle
            X += n
        else:
            cycle += 1
            if cycle >= target:
                return X * cycle

# part 1, takes in lines of file
def p1(lines):
    at_20 = get_state_at_cycle(lines, 20)
    at_60 = get_state_at_cycle(lines, 60)
    at_100 = get_state_at_cycle(lines, 100)
    at_140 = get_state_at_cycle(lines, 140)
    at_180 = get_state_at_cycle(lines, 180)
    at_220 = get_state_at_cycle(lines, 220)

    return at_20 + at_60 + at_100 + at_140 + at_180 + at_220

def format_crt(crt, sprite):
    s = "\033[1;92m\n"
    for y in range(6):
        for x in range(40):
            if sprite != -10000 and abs(sprite - (40 * y + x)) <= 1:
                s += "#" * 2
            else:
                s += crt[40 * y + x] * 2
            if crt[40 * y + x] == "X":
                s = s[:-2] + "██"

        s += "\n"

    return s + "\033[0m"

# part 2, takes in lines of file
def p2(lines):
    X = 1
    cycle = 0
    row = 0
    crt = " " * 240
    for line in lines:
        line = line.strip()
        if "addx" in line:
            s = line.split(" ")
            n = int(s[1])
            if X >= 40:
                X = 0

            if X - 1 <= (cycle) % 40 <= X + 1:
                crt = crt[:cycle] + "X" + crt[cycle + 1:]

            cycle = (cycle + 1) % 240

            if X - 1 <= (cycle) % 40 <= X + 1:
                crt = crt[:cycle] + "X" + crt[cycle + 1:]

            X += n
            cycle = (cycle + 1) % 240
        else:
            if X - 1 <= (cycle) % 40 <= X + 1:
                crt = crt[:cycle] + "X" + crt[cycle + 1:]

            cycle = (cycle + 1) % 240

            if X - 1 <= (cycle) % 240 <= X + 1:
                crt = crt[:cycle] + "X" + crt[cycle + 1:]

    print(format_crt(crt, -10000))
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

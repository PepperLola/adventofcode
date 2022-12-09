import sys
import time
import re
import itertools
import numpy as np

# shared variables here
screen = np.zeros((6, 50))

def rotate_row(r, amt):
    screen[r] = np.roll(screen[r], amt)

def rotate_col(c, amt):
    screen[:,c] = np.roll(screen[:,c], amt)

# part 1, takes in lines of file
def p1(lines):
    for line in lines:
        if "rect" in line:
            m = re.search(r"rect (\d+)x(\d+)", line)
            if m:
                for x in range(int(m.group(1))):
                    for y in range(int(m.group(2))):
                        screen[y][x] = 1
        elif "rotate" in line:
            m = re.search(r"rotate (\w+) (x|y)=(\d+) by (\d+)", line)
            if m:
                r_or_c = m.group(1)
                i = int(m.group(3))
                amt = int(m.group(4))
                if r_or_c == "row":
                    rotate_row(i, amt)
                else:
                    rotate_col(i, amt)

    return int(np.sum(screen))

# part 2, takes in lines of file
def p2(lines):
    s = "\n"
    for y in range(len(screen)):
        for x in range(len(screen[y])):
            s += "#" if screen[y][x] == 1 else " "
        s += "\n"
    return s

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

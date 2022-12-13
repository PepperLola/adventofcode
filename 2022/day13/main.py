import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np

# shared variables here
def is_right_order(a, b):
    if type(a) is int:
        if type(b) is list:
            return is_right_order([a], b)
        elif type(b) is int:
            return a < b
    elif type(a) is list:
        if type(b) is int:
            return is_right_order(a, [b])
        elif type(b) is list:
            return is_right_order_list(a, b)


def is_right_order_list(l1, l2, i = 0):
    if len(l1) == i:
        return True
    elif len(l2) == i:
        return False

    if l1[i] == l2[i]:
        return is_right_order_list(l1, l2, i + 1)
    return is_right_order(l1[i], l2[i])

# part 1, takes in lines of file
def p1(lines):
    right_order = 0
    for i in range(0, len(lines), 3):
        line1 = eval(lines[i])
        line2 = eval(lines[i + 1])
        ordered = is_right_order(line1, line2)
        if is_right_order(line1, line2):
            # print(i // 3)
            right_order += i // 3 + 1
        
    return right_order

# part 2, takes in lines of file
def p2(lines):
    l = []
    for line in lines:
        if len(line) > 0:
            l.append(eval(line))

    l = [[[2]], [[6]]] + l

    for i in range(len(l) - 1):
        for j in range(len(l) - i - 1):
            if not is_right_order(l[j], l[j+1]):
                swapped = True
                l[j], l[j+1] = l[j+1], l[j]
        if not swapped:
            break

    k = 1
    for i in range(len(l)):
        val = l[i]
        if val == [[2]] or val == [[6]]:
            k *= i + 1
    return k

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
    lines = f.read().splitlines()
    t = time.perf_counter_ns()
    a = p1(lines)
    dur = time.perf_counter_ns() - t

    print("\033[0;33m├ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

    t = time.perf_counter_ns()
    a = p2(lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

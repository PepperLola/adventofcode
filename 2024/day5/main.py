import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
import networkx as nx
from util import format_time, number_grid

# shared variables here

# part 1, takes in lines of file
def p1(file, content, lines):
    rules = []
    orders = []
    parsing_orders = False
    for line in lines:
        if line == "":
            parsing_orders = True
            continue
        if not parsing_orders:
            s = line.split("|")
            rules.append((int(s[0]), int(s[1])))
        else:
            orders.append(list(map(int, filter(lambda x: x != "", line.split(",")))))
    ret = 0
    for order in orders:
        valid = True
        for rule in rules:
            before, after = rule
            if before not in order or after not in order:
                continue
            if order.index(before) > order.index(after):
                valid = False
                break
        if valid:
            ret += order[len(order) // 2]
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    rules = []
    orders = []
    parsing_orders = False
    for line in lines:
        if line == "":
            parsing_orders = True
            continue
        if not parsing_orders:
            s = line.split("|")
            rules.append((int(s[0]), int(s[1])))
        else:
            orders.append(list(map(int, filter(lambda x: x != "", line.split(",")))))
    invalid_orders = []
    for order in orders:
        valid = True
        for rule in rules:
            before, after = rule
            if before not in order or after not in order:
                continue
            if order.index(before) > order.index(after):
                valid = False
                break
        if not valid:
            invalid_orders.append(order)
    ret = 0
    for order in invalid_orders:
        while True:
            rules_ok = 0
            for rule in rules:
                before, after = rule
                if before not in order or after not in order:
                    rules_ok += 1
                    continue
                before_idx = order.index(before)
                after_idx = order.index(after)
                if before_idx > after_idx:
                    order[before_idx], order[after_idx] = order[after_idx], order[before_idx]
                else:
                    rules_ok += 1
            if rules_ok == len(rules):
                break
        middle = order[len(order) // 2]
        ret += middle
    return ret

filename = "input.txt"

if "test" in sys.argv:
    filename = "test.txt"

with open(filename, "r") as f:
    content = f.read()
    lines = content.splitlines()
    t = time.perf_counter_ns()
    a = p1(f, content, lines)
    dur = time.perf_counter_ns() - t

    print("\033[0;33m├ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

    t = time.perf_counter_ns()
    a = p2(f, content, lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

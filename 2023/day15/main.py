import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid

# shared variables here
def hash_char(c, v):
    return ((v + ord(c)) * 17) % 256
def hash(s):
    curr = 0
    for c in s:
        curr = hash_char(c, curr)
    return curr

# part 1, takes in lines of file
def p1(file, content, lines):
    line = lines[0]
    total = 0
    for s in line.split(","):
        total += hash(s)
    return total

# part 2, takes in lines of file
def p2(file, content, lines):
    line = lines[0]
    hashmap = {}
    for s in line.split(","):
        if "=" in s:
            bn, v = s.split("=")
            b = hash(bn)
            if not b in hashmap.keys():
                hashmap[b] = [[bn, v]]
            else:
                if bn in map(lambda x: x[0], hashmap[b]):
                    for e in hashmap[b]:
                        if e[0] == bn:
                            e[1] = v
                else:
                    hashmap[b].append([bn, v])
        elif "-" in s:
            bn, v = s.split("-")
            b = hash(bn)
            if not b in hashmap.keys():
                hashmap[b] = [[bn, v]]
            else:
                hashmap[b] = list(filter(lambda x: x[0] != bn, hashmap[b]))
    total = 0
    for b in hashmap.keys():
        for (i, v) in enumerate(hashmap[b]):
            p = (int(b)+1) * (i+1) * int(v[1])
            total += p
    return total

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

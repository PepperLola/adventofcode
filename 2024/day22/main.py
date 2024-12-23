import sys
import time
import re
import itertools
import more_itertools
from collections import defaultdict, deque, Counter
import math
import copy
import numpy as np
import networkx as nx
from util import format_time, number_grid

# shared variables here
def mix(n1, n2):
    return n1 ^ n2

def prune(num):
    return num & 0xFFFFFF

def next(num) -> int:
    num = mix(num, num * 64)
    num = prune(num)
    num = mix(num, num // 32)
    num = prune(num)
    num = mix(num, num * 2048)
    return prune(num)

# part 1, takes in lines of file
def p1(file, content, lines):
    ret = 0
    for line in lines:
        n = int(line)
        for _ in range(2000):
            n = next(n)
        ret += n
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    per_buyer: list[dict[tuple[int], int]] = []
    all_seqs = set()
    for line in lines:
        n = int(line)
        res: list[tuple[int, int]] = []
        seqs = defaultdict()
        for _ in range(2000):
            prev = n % 10
            n = next(n)
            res.append((n, n % 10 - prev))
        for window in more_itertools.sliding_window(res, 4):
            r = window[3][0]%10
            seq = tuple(x[1] for x in window)
            all_seqs.add(seq)
            if seq not in seqs:
                seqs[seq] = r
        per_buyer.append(seqs)

    highest = 0
    for seq in all_seqs:
        total = 0
        for sl in per_buyer:
            if seq not in sl:
                continue
            total += sl[seq]
        highest = max(total, highest)
    return highest

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

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
    q = deque()
    for i, c in enumerate(lines[0]):
        q.append((i // 2, int(c), i % 2 == 1)) # id, len, empty
    final = []
    while len(q) > 0:
        left = q.popleft()
        if not left[2]:
            for i in range(left[1]):
                final.append(left[0])
        else:
            if len(q) == 0:
                break
            right = q.pop()
            while right[2] and len(q) > 0:
                right = q.pop()
            m = min(left[1], right[1])
            for i in range(m):
                final.append(right[0])
            if left[1] < right[1]:
                q.append((right[0], right[1] - left[1], False))
            elif right[1] < left[1]:
                q.appendleft((left[0], left[1]-right[1], True))
    return sum([i*c for i, c in enumerate(final)])

# part 2, takes in lines of file
def p2(file, content, lines):
    spaces = []
    files = deque()
    pos = 0
    final = []
    fid = 0
    for i, c in enumerate(lines[0]):
        if i % 2 == 0:
            files.append((i // 2, int(c), pos)) # id, len, pos
            for j in range(int(c)):
                final.append(i // 2)
        else:
            spaces.append((int(c), pos))
            for i in range(int(c)):
                final.append(None)
        pos += int(c)
    for i, f in enumerate(reversed(files)):
        fid, flen, fpos = f
        for si, s in enumerate(spaces):
            slen, spos = s
            if spos < fpos and slen >= flen:
                for i in range(flen):
                    final[fpos+i] = None
                    final[spos+i] = fid
                spaces[si] = (slen - flen, spos + flen)
                break
    ret = 0
    for i, c in enumerate(final):
        if c is not None:
            ret += i * c
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

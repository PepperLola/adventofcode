import sys
import time
import re
import itertools
from collections import defaultdict, deque, Counter
import math
import copy
import numpy as np
import networkx as nx
from util import format_time, number_grid
from functools import cache
from scipy.optimize import LinearConstraint, milp

# shared variables here
inds = []
btns = []
jrs = []

def apply_press(ind, btn):
    n = copy.deepcopy(ind)
    for i in btn:
        n[i] = not ind[i]
    return n

def bfs(target, ind, btn_opts):
    visited = []
    q = deque()
    for btn in btn_opts:
        x = (ind, [btn])
        q.append(x)
        visited.append(ind)
    while q:
        oind, obtns = q.popleft()
        app = apply_press(oind, obtns[-1])
        if tuple(app) == target:
            return app, obtns
        if app not in visited:
            for nbtn in btn_opts:
                n = (app, [*obtns, nbtn])
                q.append(n)
            visited.append(app)
    return -1, []

# part 1, takes in lines of file
def p1(file, content, lines):
    global inds, btns, jrs

    for line in lines:
        s = line.split(" ")
        ind, *btn = s[:-1]
        jr = s[-1]
        jr = tuple(map(int, jr[1:-1].split(",")))

        ind = tuple(map(lambda x: x == "#", ind[1:-1]))

        nbtn = list(map(lambda x: tuple(map(int, x[1:-1].split(","))), btn))

        inds.append(ind)
        btns.append(nbtn)
        jrs.append(jr)

    ret = 0
    for i in range(len(inds)):
        ind = inds[i]
        btn_opts = btns[i]
        
        oind, obtns = bfs(ind, [False]*len(ind), btn_opts)
        ret += len(obtns)

    return ret

def btn_to_vec(btn, veclen):
    arr = [0] * veclen
    for i in btn:
        arr[i] = 1
    return arr

# part 2, takes in lines of file
def p2(file, content, lines):
    global inds, btns, jrs
    ret = 0

    for i, jr in enumerate(jrs):
        btn_opts = btns[i]

        btn_vecs = np.array(list(map(lambda x: btn_to_vec(x, len(jr)), btn_opts))).T

        linear_constraint = LinearConstraint(btn_vecs, jr, jr)
        result = milp(
            c=np.ones(btn_vecs.shape[1]),
            constraints=linear_constraint,
            integrality=1
        )
        ret += sum(result.x)

    return int(ret)

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

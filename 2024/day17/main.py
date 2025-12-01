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

# shared variables here
reg = {}
prog = []

def combo(op):
    if 0 <= op <= 3:
        return op
    elif op == 4:
        return reg['A']
    elif op == 5:
        return reg['B']
    elif op == 6:
        return reg['C']
    return -1

# part 1, takes in lines of file
def p1(file, content, lines):
    global reg, prog
    for line in lines:
        if "Register" in line:
            r = line[len("Register ")]
            v = int(line[len("Register A: "):])
            reg[r] = v
        elif "Program" in line:
            prog = list(map(int, line[len("Program: "):].split(",")))
    regc = copy.deepcopy(reg)
    for A in itertools.count(1000000000000):
        print(A, end="\r")
        reg = regc
        reg['A'] = A
        pc = 0
        out = []
        while pc < len(prog):
            inst, val = prog[pc:pc+2]
            # print(pc, inst, val, reg)
            # input()
            if inst == 0:
                reg['A'] = reg['A'] // int(2 ** combo(val))
            elif inst == 1:
                reg['B'] = reg['B'] ^ val
            elif inst == 2:
                reg['B'] = combo(val) % 8
            elif inst == 3:
                if reg['A'] != 0:
                    pc = val
                    continue
            elif inst == 4:
                reg['B'] = reg['B'] ^ reg['C']
            elif inst == 5:
                out.append(combo(val) % 8)
            elif inst == 6:
                reg['B'] = int(reg['A'] // int(2 ** combo(val)))
            elif inst == 7:
                reg['C'] = int(reg['A'] // int(2 ** combo(val)))
            pc += 2
        if out == prog:
            return A
            return ",".join(map(str, out))
    return 0
    return ",".join(map(str, out))

# part 2, takes in lines of file
def p2(file, content, lines):
    return 0

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

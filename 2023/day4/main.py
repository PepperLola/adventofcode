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

# part 1, takes in lines of file
def p1(file, content, lines):
    total = 0
    for line in lines:
        line = line[line.index(":") + 1:].replace("  ", " ")
        if line[0] == " ":
            line = line[1:]
        points = 0
        split = line.split(" | ")
        win = [int(i) for i in split[0].split(" ")]
        yours = [int(i) for i in split[1].split(" ")]
        for y in yours:
            if y in win:
                if points > 0:
                    points *= 2
                else:
                    points = 1
        total += points
    return total

# part 2, takes in lines of file
def p2(file, content, lines):
    cards = {  }
    p = re.compile(r"Card +(\d+): +")
    for line in lines:
        line = line.replace("  ", " ")
        id = p.search(line).group(1)
        line = line[line.index(":") + 1:]
        if line[0] == " ":
            line = line[1:]
        split = line.split(" | ")
        yours = [int(i) for i in split[1].split(" ")]
        winning = [int(i) for i in split[0].split(" ")]
        cards[int(id)] = len([i for i in yours if i in winning])
    copies = {}
    std = sorted(list(cards.keys()), reverse=True)
    for id in std:
        copies[id] = 1 + sum([copies[i] for i in range(id+1, id+cards[id]+1)])
    return sum(copies.values())

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

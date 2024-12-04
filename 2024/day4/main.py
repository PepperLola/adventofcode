import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, letter_grid, number_grid

# shared variables here

# part 1, takes in lines of file
def p1(file, content, lines):
    grid = letter_grid(lines)
    ret = 0
    for j in range(len(grid)):
        for i in range(len(grid[j])):
            if j >= 3:
                if grid[j][i] == 'X' and grid[j-1][i] == 'M' and grid[j-2][i] == 'A' and grid[j-3][i] == 'S':
                    ret += 1
            if j <= len(grid) - 4:
                if grid[j][i] == 'X' and grid[j+1][i] == 'M' and grid[j+2][i] == 'A' and grid[j+3][i] == 'S':
                    ret += 1
            if i >= 3:
                if grid[j][i] == 'X' and grid[j][i-1] == 'M' and grid[j][i-2] == 'A' and grid[j][i-3] == 'S':
                    ret += 1
            if i <= len(grid[j]) - 4:
                if grid[j][i] == 'X' and grid[j][i+1] == 'M' and grid[j][i+2] == 'A' and grid[j][i+3] == 'S':
                    ret += 1
            if i >= 3 and j >= 3:
                if grid[j][i] == 'X' and grid[j-1][i-1] == 'M' and grid[j-2][i-2] == 'A' and grid[j-3][i-3] == 'S':
                    ret += 1
            if i <= len(grid[j]) - 4 and j >= 3:
                if grid[j][i] == 'X' and grid[j-1][i+1] == 'M' and grid[j-2][i+2] == 'A' and grid[j-3][i+3] == 'S':
                    ret += 1
            if i >= 3 and j <= len(grid) - 4:
                if grid[j][i] == 'X' and grid[j+1][i-1] == 'M' and grid[j+2][i-2] == 'A' and grid[j+3][i-3] == 'S':
                    ret += 1
            if i <= len(grid[j]) - 4 and j <= len(grid) - 4:
                if grid[j][i] == 'X' and grid[j+1][i+1] == 'M' and grid[j+2][i+2] == 'A' and grid[j+3][i+3] == 'S':
                    ret += 1
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    ret = 0
    grid = letter_grid(lines)
    for j in range(len(grid) - 2):
        for i in range(len(grid[j]) - 2):
            if grid[j+1][i+1] == 'A' and ((grid[j][i] == 'M' and grid[j+2][i+2] == 'S') or (grid[j][i] == 'S' and grid[j+2][i+2] == 'M')) and ((grid[j+2][i] == 'M' and grid[j][i+2] == 'S') or (grid[j+2][i] == 'S' and grid[j][i+2] == 'M')):
                ret += 1
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

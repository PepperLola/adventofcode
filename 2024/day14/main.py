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
robots = []
W = 101
H = 103

# part 1, takes in lines of file
def p1(file, content, lines):
    global robots, W, H
    for line in lines:
        px, py, vx, vy = map(int, re.findall(r"(-?\d+)", line))
        robots.append(( [ px, py ], (vx, vy) ))
    r = copy.deepcopy(robots)
    for _ in range(100):
        for robot in r:
            vx, vy = robot[1]
            robot[0][0] += vx
            robot[0][1] += vy
            if robot[0][0] < 0:
                robot[0][0] += W
            if robot[0][1] < 0:
                robot[0][1] += H
            if robot[0][0] >= W:
                robot[0][0] -= W
            if robot[0][1] >= H:
                robot[0][1] -= H
    qs = [0, 0, 0, 0]
    for (px, py), (_, _) in r:
        if px > W // 2 and py > H // 2:
            qs[2] += 1
        elif px > W // 2 and py < H // 2:
            qs[1] += 1
        elif px < W // 2 and py > H // 2:
            qs[3] += 1
        elif px < W // 2 and py < H // 2:
            qs[0] += 1
    return int(np.prod(qs))

def print_robots(robots, W, H):
    r = set()
    for robot in robots:
        r.add(tuple(robot[0]))
    for y in range(H):
        s = ""
        for x in range(W):
            if (x, y) in r:
                s += "#"
            else:
                s += "."
        print(s)

def positions_occupied(robots):
    return set(map(lambda robot: tuple(robot[0]), robots))

# part 2, takes in lines of file
def p2(file, content, lines):
    global robots, W, H
    for i in range(10000):
        for robot in robots:
            vx, vy = robot[1]
            robot[0][0] += vx
            robot[0][1] += vy
            if robot[0][0] < 0:
                robot[0][0] += W
            if robot[0][1] < 0:
                robot[0][1] += H
            if robot[0][0] >= W:
                robot[0][0] -= W
            if robot[0][1] >= H:
                robot[0][1] -= H

        # I originally just printed out the board every iteration, saved it to a file,
        # and stepped through it in VSCode with the VSCode minimap
        ### print(i+1)
        ### print_robots(robots, W, H)
        # I saw this trick on Reddit and used it so I can still print out the answer
        if len(robots) == len(positions_occupied(robots)):
            return i + 1
    return -1

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

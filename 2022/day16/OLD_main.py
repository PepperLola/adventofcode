import sys
import time
import re
import itertools
from collections import defaultdict, deque, namedtuple
import math
import copy
import numpy as np

# shared variables here
Pipe = namedtuple("Pipe", ["name", "rate", "valves"])

# def shortest_path(p1, p2, pipes, visited = set(), depth = 0):
    # ds = []
    # test = defaultdict(int)
    # visited.add(p1)
    # print(depth, p1, p2, visited)
    # if p1 == p2:
        # return 0
    # for valve in pipes[p1].valves:
        # # if valve == p2:
            # # print(p1, "HAS", p2, "AS A NEIGHBOR!!")
            # # ds.append(0)
        # if not valve in visited:
            # print("FINDING SHORTEST PATH BETWEEN", valve, p2)
            # p = shortest_path(valve, p2, pipes, copy.deepcopy(visited), depth + 1)
            # print("DIST FROM", valve, "TO", p2, p)
            # ds.append(p)
        # input()
    # print(ds)
    # input()
    # return 1 + (min(ds) if len(ds) > 0 else 100000)

def shortest_path(p1, p2, pipes):
    q = deque()
    q.append((p1, 0))
    while q:
        n, d = q.popleft()
        if not p2 in pipes[n].valves:
            for p in pipes[n].valves:
                q.append((p, d + 1))
        else:
            return d + 1

# part 1, takes in lines of file
def p1(lines):
    pipes = defaultdict(tuple)
    for line in lines:
        m = re.search(r"Valve (\w+) has flow rate=(-?\d+); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.*)", line)
        if m:
            valve = m.group(1)
            rate = int(m.group(2))
            others = m.group(3).split(", ")
            pipe = Pipe(valve, rate, others)
            pipes[valve] = pipe
    
    print(shortest_path("AA", "HH", pipes))

    pressure = 0
    opened = set()
    queued_moves = -1
    fro = "AA"
    for i in range(30):
        curr_pressure = 0
        for o in opened:
            curr_pressure += pipes[o].rate
        # print(i + 1, curr_pressure, fro, opened)
        # input()
        pressure += curr_pressure
        if queued_moves == -1:
            non_zero = {x for x in list(pipes.keys()) if pipes[x].rate > 0}
            sorted_non_zero = sorted(list(non_zero), key=lambda x: pipes[x].rate, reverse=True)
            dists = defaultdict(int)
            max_dist = -1
            for pipe in sorted_non_zero:
                dist = shortest_path(fro, pipe, pipes)
                # print(fro, pipe, dist, path)
                if dist > max_dist:
                    max_dist = dist
                dists[pipe] = dist
            weighted = defaultdict(int)
            for pipe in sorted_non_zero:
                weighted[pipe] = pipes[pipe].rate * ((max_dist - dists[pipe]) if dists[pipe] != max_dist else 1)
            target = sorted_non_zero[0]
            if not all([dists[x] == max_dist for x in sorted_non_zero]):
                weight_sorted = sorted(weighted.keys(), key=lambda x: weighted[x], reverse=True)
                targets = list(filter(lambda x: not x in opened, weight_sorted))
                if len(targets) == 0:
                    continue
                else:
                    target = targets[0]
            queued_moves = dists[target] - 1
            # print(target, dists[target], queued_moves)
            fro = target
        else:
            if queued_moves == 0:
                opened.add(fro)
            queued_moves -= 1

    return pressure

# part 2, takes in lines of file
def p2(lines):
    return 0

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

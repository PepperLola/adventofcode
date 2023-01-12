import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np

# shared variables here
cache = {}

def dfs(valves, dists, indices, time, valve, visited):
    if (time, valve, visited) in cache:
        return cache[(time, valve, visited)]

    maxv = 0
    for neighbor in dists[valve]:
        test_bit = 1 << indices[neighbor]
        if visited & test_bit:
            continue
        remaining = time - dists[valve][neighbor] - 1
        if remaining <= 0:
            continue
        maxv = max(maxv, dfs(valves, dists, indices, remaining, neighbor, visited | test_bit) + valves[neighbor] * remaining)

    cache[(time, valve, visited)] = maxv
    return maxv

# part 1, takes in lines of file
def p1(lines):
    valves = {}
    tunnels = {}

    for line in lines:
        m = re.search(r"Valve (\w+) has flow rate=(-?\d+); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.*)", line)
        if m:
            valve = m.group(1)
            rate = int(m.group(2))
            others = m.group(3).split(", ")
            valves[valve] = rate
            tunnels[valve] = others
    
    dists = {}
    nonempty = []

    for valve in valves:
        if valve != "AA" and not valves[valve]:
            continue

        if valve != "AA":
            nonempty.append(valve)

        dists[valve] = {valve: 0, "AA": 0}
        visited = {valve}

        queue = deque([(0, valve)])

        while queue:
            distance, position = queue.popleft()
            for neighbor in tunnels[position]:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                if valves[neighbor]:
                    dists[valve][neighbor] = distance + 1
                queue.append((distance + 1, neighbor))

        del dists[valve][valve]
        if valve != "AA":
            del dists[valve]["AA"]

    indices = {}

    for index, element in enumerate(nonempty):
        indices[element] = index

    return dfs(valves, dists, indices, 30, "AA", 0)

# part 2, takes in lines of file
def p2(lines):
    valves = {}
    tunnels = {}

    for line in lines:
        m = re.search(r"Valve (\w+) has flow rate=(-?\d+); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.*)", line)
        if m:
            valve = m.group(1)
            rate = int(m.group(2))
            others = m.group(3).split(", ")
            valves[valve] = rate
            tunnels[valve] = others
    
    dists = {}
    nonempty = []

    for valve in valves:
        if valve != "AA" and not valves[valve]:
            continue

        if valve != "AA":
            nonempty.append(valve)

        dists[valve] = {valve: 0, "AA": 0}
        visited = {valve}

        queue = deque([(0, valve)])

        while queue:
            distance, position = queue.popleft()
            for neighbor in tunnels[position]:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                if valves[neighbor]:
                    dists[valve][neighbor] = distance + 1
                queue.append((distance + 1, neighbor))

        del dists[valve][valve]
        if valve != "AA":
            del dists[valve]["AA"]

    indices = {}

    for index, element in enumerate(nonempty):
        indices[element] = index

    all_valves = (1 << len(nonempty)) - 1

    minv = 0

    # find the max combination of us visiting some and elephant visiting rest
    for i in range((all_valves + 1) // 2):
        elephant = dfs(valves, dists, indices, 26, "AA", i)
        us = dfs(valves, dists, indices, 26, "AA", all_valves ^ i)
        minv = max(minv, elephant + us)

    return minv

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

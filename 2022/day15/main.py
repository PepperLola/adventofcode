import sys
import time
import re
import itertools
from collections import defaultdict, deque
import math
import copy
import numpy as np

# shared variables here
def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# part 1, takes in lines of file
def p1(lines):
    sensors = defaultdict(tuple)
    target_y = 2000000
    target_beacon = (0, 0)
    closest_sensors = []
    for line in lines:
        m = re.search(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        if m:
            sensor_pos = (int(m.group(1)), int(m.group(2)))
            closest_beacon = (int(m.group(3)), int(m.group(4)))
            sensors[sensor_pos] = closest_beacon
            if closest_beacon[1] == target_y:
                target_beacon = closest_beacon
                closest_sensors.append(sensor_pos)

    closest_sensors.sort(key=lambda x: distance(closest_beacon, x))
    row_coverage = set()
    for sensor in sensors.keys():
        x_dist = abs(sensors[sensor][0] - sensor[0])
        y_dist = abs(sensors[sensor][1] - sensor[1])
        x_width_at_sensor = x_dist*2+1 + y_dist * 2
        y_dist_to_target = abs(sensor[1] - target_y)
        x_width_at_target = x_width_at_sensor - 2*abs(sensor[1] - target_y)
        for x in range(sensor[0] - (x_width_at_target // 2), sensor[0] + (x_width_at_target // 2 + 1)):
            row_coverage.add((x, target_y))

    return len(row_coverage) - len(list(filter(lambda x: x in sensors.values() and x[1] == target_y, row_coverage)))

def filter_grid(p, dists):
    for sensor in dists.keys():
        if distance(p, sensor) <= dists[sensor]:
            return False
    return True


# part 2, takes in lines of file
def p2(lines):
    sensors = defaultdict(tuple)
    for line in lines:
        m = re.search(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        if m:
            sensor_pos = (int(m.group(1)), int(m.group(2)))
            closest_beacon = (int(m.group(3)), int(m.group(4)))
            sensors[sensor_pos] = closest_beacon

    coverage = set()
    dists = defaultdict(int)
    for sensor in sensors.keys():
        dists[sensor] = distance(sensor, sensors[sensor])

    filtered = set()
    for sensor in sensors.keys():
        for dx in range(dists[sensor] + 2):
            dy = (dists[sensor] + 1) - dx
            directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
            for sx, sy in directions:
                x = sensor[0] + (dx * sx)
                y = sensor[1] + (dy * sy)
                if not (0 <= x <= 4000000 and 0 <= y <= 4000000):
                    continue
                if filter_grid((x, y), dists):
                    return (x*4000000 + y)

    return list(pt)[0]

    # return len(row_coverage) - len(list(filter(lambda x: x in sensors.values() and x[1] == target_y, coverage)))

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

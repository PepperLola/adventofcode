import sys
import time
import re
import itertools

# shared variables here
dists = {}

def find_distances(cities):
    cities = list(cities)
    dist = 0
    for i in range(1, len(cities)):
        city1, city2 = cities[i-1:i+1]
        if (city1, city2) in dists:
            dist += dists[(city1, city2)]
        else:
            dist += dists[(city2, city1)]

    return dist

# part 1, takes in lines of file
def p1(lines):
    cities = set()
    for line in lines:
        match = re.search(r"(\w+) to (\w+) = (\d+)", line)
        if match:
            city1, city2, dist = match.group(1), match.group(2), int(match.group(3))
            dists[(city1, city2)] = dist
            cities.add(city1)
            cities.add(city2)

    perms = itertools.permutations(cities)

    routes = []
    for route in perms:
        routes.append(find_distances(route))

    return min(routes)

# part 2, takes in lines of file
def p2(lines):
    cities = set()
    for line in lines:
        match = re.search(r"(\w+) to (\w+) = (\d+)", line)
        if match:
            city1, city2, dist = match.group(1), match.group(2), int(match.group(3))
            dists[(city1, city2)] = dist
            cities.add(city1)
            cities.add(city2)

    perms = itertools.permutations(cities)

    routes = []
    for route in perms:
        routes.append(find_distances(route))

    return max(routes)

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
    lines = f.readlines()
    t = time.perf_counter_ns()
    a = p1(lines)
    dur = time.perf_counter_ns() - t

    print("\033[0;33m├ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

    t = time.perf_counter_ns()
    a = p2(lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

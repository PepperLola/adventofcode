import sys
import time
import re

# shared variables here
actual = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1
}

# part 1, takes in lines of file
def p1(lines):
    for line in lines:
        sue = line[4:line.index(":")]
        stats = line[line.index(":") + 2:].strip().split(", ")
        stats_correct = 0
        stat_dict = {}
        for stat in stats:
            s = stat.split(": ")
            stat_dict[s[0]] = int(s[1])
        for stat in stat_dict.items():
            if actual[stat[0]] == stat[1]:
                stats_correct += 1

        if stats_correct == len(stat_dict):
            return sue

    return 0

# part 2, takes in lines of file
def p2(lines):
    for line in lines:
        sue = line[4:line.index(":")]
        stats = line[line.index(":") + 2:].strip().split(", ")
        stats_correct = 0
        stat_dict = {}
        for stat in stats:
            s = stat.split(": ")
            stat_dict[s[0]] = int(s[1])
        for stat in stat_dict.items():
            if stat[0] in ["cats", "trees"]:
                if actual[stat[0]] < stat[1]:
                    stats_correct += 1
            elif stat[0] in ["pomeranians", "goldfish"]:
                if actual[stat[0]] > stat[1]:
                    stats_correct += 1
            elif actual[stat[0]] == stat[1]:
                stats_correct += 1

        if stats_correct == len(stat_dict):
            return sue

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
    lines = f.readlines()
    t = time.perf_counter_ns()
    a = p1(lines)
    dur = time.perf_counter_ns() - t

    print("\033[0;33m├ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

    t = time.perf_counter_ns()
    a = p2(lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

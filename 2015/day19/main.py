import sys
import time
import re
import itertools
import numpy as np
from random import sample

# shared variables here

# part 1, takes in lines of file
def p1(lines):
    replacements = {}
    molecule = ""
    for line in lines:
        if " => " in line:
            s = line.split(" => ")
            if not s[0] in replacements:
                replacements[s[0]] = []
            if not s[1] in replacements[s[0]]:
                replacements[s[0]].append(s[1].strip())
        elif len(line) > 1:
            molecule = line.strip()

    possibilities = set()
    substitutors = list(replacements.keys())
    for sub in substitutors:
        indices = [i.start() for i in re.finditer(sub, molecule)]
        for idx in indices:
            for replacer in replacements[sub]:
                with_sub = molecule[:idx] + replacer + molecule[idx + len(sub):]
                possibilities.add(with_sub)
                # print(molecule, sub, idx, replacer, with_sub, possibilities)

    return len(possibilities)

# part 2, takes in lines of file
def p2(lines):
    replacements = {}
    molecule = ""
    for line in lines:
        if " => " in line:
            s = line.split(" => ")
            replacements[s[1].strip()] = s[0]
        elif len(line) > 1:
            molecule = line.strip()

    i = 0
    final = molecule
    replacement_keys = list(replacements.keys())
    num_replacements = len(replacements)
    while final != "e":
        temp = final
        for n in sample(replacement_keys, num_replacements):
            if n in final:
                i += final.count(n)
                final = final.replace(n, replacements[n])

        if final == temp:
            final = molecule
            i = 0
            continue


    return i

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

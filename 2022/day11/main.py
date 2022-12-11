import sys
import time
import re
import itertools
import numpy as np

# shared variables here

# part 1, takes in lines of file
def p1(lines):
    monkeys = []
    monkey = -1
    for line in lines:
        line = line.strip()
        if "Monkey" in line:
            monkey += 1
            monkeys.append({})
        elif "Starting" in line:
            monkeys[monkey]['items'] = [int(i) for i in line.split(": ")[1].split(", ")]
        elif "Operation" in line:
            monkeys[monkey]['operation'] = line.split(": ")[1].split(" = ")[1]
        elif "Test" in line:
            monkeys[monkey]['test'] = int(line.split(": ")[1].split(" ")[-1])
        elif "true" in line:
            monkeys[monkey]['onTrue'] = int(line.split(": ")[1].split(" ")[-1])
        elif "false" in line:
            monkeys[monkey]['onFalse'] = int(line.split(": ")[1].split(" ")[-1])

    inspected = [0 for i in range(len(monkeys))]

    for r in range(20):
        for i in range(len(monkeys)):
            monkey = monkeys[i]
            while len(monkey['items']) > 0:
                item = monkey['items'][0]
                inspected[i] += 1
                monkey['items'][0] = eval(monkey['operation'].replace("old", str(item)))
                monkey['items'][0] = monkey['items'][0] // 3
                if monkey['items'][0] % monkey['test'] == 0:
                    monkeys[monkey['onTrue']]['items'].append(monkey['items'][0])
                else:
                    monkeys[monkey['onFalse']]['items'].append(monkey['items'][0])
                monkey['items'] = monkey['items'][1:]

    return np.prod(sorted(inspected, reverse=True)[:2])

# part 2, takes in lines of file
def p2(lines):
    monkeys = []
    monkey = -1
    for line in lines:
        line = line.strip()
        if "Monkey" in line:
            monkey += 1
            monkeys.append({})
        elif "Starting" in line:
            monkeys[monkey]['items'] = [int(i) for i in line.split(": ")[1].split(", ")]
        elif "Operation" in line:
            monkeys[monkey]['operation'] = line.split(": ")[1].split(" = ")[1]
        elif "Test" in line:
            monkeys[monkey]['test'] = int(line.split(": ")[1].split(" ")[-1])
        elif "true" in line:
            monkeys[monkey]['onTrue'] = int(line.split(": ")[1].split(" ")[-1])
        elif "false" in line:
            monkeys[monkey]['onFalse'] = int(line.split(": ")[1].split(" ")[-1])

    inspected = [0 for i in range(len(monkeys))]
    lcm = 1 # keep track of lcm of all tests to keep the number smaller
    # we can mod by this lcm and preserve all of the tests
    for m in monkeys:
        lcm *= m['test']

    for r in range(10000):
        print(f"Processing round {str(r).zfill(5)}/10000", end="\r")
        for m in range(len(monkeys)):
            monkey = monkeys[m]
            for i in range(len(monkey['items'])):
                inspected[m] += 1
                monkey['items'][i] %= lcm
                op = monkey['operation'].replace("old", str(monkey['items'][i]))
                monkey['items'][i] = eval(op)
                if monkey['items'][i] % monkey['test'] == 0:
                    monkeys[monkey['onTrue']]['items'].append(monkey['items'][i] % lcm) # mod by lcm to keep the number small
                else:
                    monkeys[monkey['onFalse']]['items'].append(monkey['items'][i] % lcm)
            monkey['items'] = []

    return np.prod(sorted(inspected, reverse=True)[:2])

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

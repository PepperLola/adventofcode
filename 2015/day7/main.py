import sys
import time
import re
from collections import namedtuple

# shared variables here
wires = {}

def init_wires(lines):
    for line in lines:
        if " -> " in line:
            match = re.search(r"(.+) -> ([\w\d]+)", line)
            wires[match.group(2)] = match.group(1)

def process_op(op, val1, val2 = 0):
    if op == "NOT":
        return ~val1
    elif op == "AND":
        return val1 & val2
    elif op == "OR":
        return val1 | val2
    elif op == "LSHIFT":
        return val1 << val2
    elif op == "RSHIFT":
        return val1 >> val2

def evaluate_wire(wire):
    if isinstance(wire, int) or wire.isnumeric():
        return int(wire)
    inst = wires[wire]
    if isinstance(inst, int) or inst.isnumeric():
        return int(inst)

    if not " " in inst: #just direct wire set
        wires[wire] = evaluate_wire(inst)
    else:
        if "NOT" in inst:
            match = re.search(r"^NOT ([\w\d]+)", inst)
            if  match:
                wires[wire] = process_op("NOT", evaluate_wire(match.group(1)))
        else:
            match = re.search(r"^([\w\d]+) (\w+) ([\w\d]+)", inst)
            if match:
                wire1 = match.group(1)
                wire2 = match.group(3)
                op = match.group(2)
                wires[wire] = process_op(op, evaluate_wire(wire1), evaluate_wire(wire2))
    return wires[wire]

# part 1, takes in lines of file
def p1(lines):
    init_wires(lines)
    return evaluate_wire("a")


# part 2, takes in lines of file
def p2(lines):
    a = evaluate_wire("a")
    init_wires(lines)
    wires['b'] = a
    return evaluate_wire("a")

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

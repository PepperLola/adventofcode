import sys
import time
import re
import itertools
import numpy as np

# shared variables here
def process_registers(registers, lines):
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # print(i, line, registers)
        # input()
        inst = line.replace(",", "").split(" ")

        if inst[0] == "hlf":
            registers[inst[1]] /= 2
        elif inst[0] == "tpl":
            registers[inst[1]] *= 3
        elif inst[0] == "inc":
            registers[inst[1]] += 1
        elif inst[0] == "jmp":
            i += int(inst[1]) - 1
        elif inst[0] == "jie":
            offset = int(inst[2])
            if registers[inst[1]] % 2 == 0:
                    i += offset - 1
        elif inst[0] == "jio":
            offset = int(inst[2])
            if registers[inst[1]] == 1:
                i += offset - 1
        i += 1

# part 1, takes in lines of file
def p1(lines):
    registers = {"a": 0, "b": 0}
    process_registers(registers, lines)
    return registers["b"]

# part 2, takes in lines of file
def p2(lines):
    registers = {"a": 1, "b": 0}
    process_registers(registers, lines)
    return registers["b"]

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

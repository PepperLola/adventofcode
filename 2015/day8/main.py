import sys
import time
import re

# shared variables here

# part 1, takes in lines of file
def p1(lines):
    literal_chrs = 0
    mem_chrs = 0

    for line in lines:
        literal_chrs += len(line)
        l = bytes(line[1:len(line) - 1], 'utf-8').decode('unicode_escape')
        mem_chrs += len(l)

    return literal_chrs - mem_chrs

# part 2, takes in lines of file
def p2(lines):
    literal_chrs = 0
    new_literal_chrs = 0

    for line in lines:
        literal_chrs += len(line)
        l = "\"" + line.replace("\\", "\\\\").replace("\"", "\\\"") + "\""
        new_literal_chrs += len(l)
    return new_literal_chrs - literal_chrs

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

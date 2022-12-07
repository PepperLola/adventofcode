import sys
import time
import re
import json

# shared variables here

# part 1, takes in lines of file
def p1(lines):
    file = "".join(lines)
    match = re.findall("-?\d+", file)
    return sum([int(i) for i in match])

def sum_object(o):
    temp_sum = 0
    if type(o) is str:
        return 0
    elif type(o) is int:
        return o
    elif type(o) is list:
        for i in o:
            temp_sum += sum_object(i)
    elif type(o) is dict:
        if "red" in o.values():
            return 0
        for key in o.keys():
            temp_sum += sum_object(o[key])
    return temp_sum


# part 2, takes in lines of file
def p2(lines):
    y = json.loads(lines[0])
    return sum_object(y)

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

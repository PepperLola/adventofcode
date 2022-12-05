import sys
import time
import re

# shared variables here

# part 1, takes in lines of file
def p1(lines):
    lit_lights = {}
    for line in lines:
        coords = [int(i) for i in re.findall("\d+", line)]
        for x in range(coords[0], coords[2] + 1):
            for y in range(coords[1], coords[3] + 1):
                # print((x, y))
                if "turn on" in line:
                    lit_lights[(x, y)] = 1
                elif "turn off" in line:
                    if (x, y) in lit_lights:
                        del lit_lights[(x, y)]
                elif "toggle" in line:
                    if (x, y) in lit_lights:
                        del lit_lights[(x, y)]
                    else:
                        lit_lights[(x, y)] = 1
    return len(lit_lights.keys())

# part 2, takes in lines of file
def p2(lines):
    lit_lights = {}
    for line in lines:
        coords = [int(i) for i in re.findall("\d+", line)]
        for x in range(coords[0], coords[2] + 1):
            for y in range(coords[1], coords[3] + 1):
                # print((x, y))
                if "turn on" in line:
                    lit_lights[(x, y)] = (lit_lights[(x, y)] if (x, y) in lit_lights else 0) + 1
                elif "turn off" in line:
                    if (x, y) in lit_lights:
                        if lit_lights[(x, y)] == 1:
                            del lit_lights[(x, y)]
                        else:
                            lit_lights[(x, y)] -= 1
                elif "toggle" in line:
                    lit_lights[(x, y)] = (lit_lights[(x, y)] if (x, y) in lit_lights else 0) + 2
    return sum(lit_lights.values())

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

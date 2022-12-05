import sys
import time

# shared variables here

# part 1, takes in lines of file
def p1(lines):
    line = lines[0]
    seen = 1
    houses = {(0, 0): 1}
    x = 0
    y = 0
    for c in line:
        if c == ">":
            x += 1
        elif c == "<":
            x -= 1
        elif c == "^":
            y += 1
        elif c == "v":
            y -= 1

        if not (x, y) in houses:
            seen += 1
            houses[(x, y)] = 1
    return seen

# part 2, takes in lines of file
def p2(lines):
    line = lines[0]
    seen = 1
    houses = {(0, 0): 1}
    x1, y1 = 0, 0 #santa
    x2, y2 = 0, 0 #robo-santa
    santa = 0 #0 = santa, 1 = robo-santa
    for c in line:
        dx = 0
        dy = 0

        if c == ">":
            dx += 1
        elif c == "<":
            dx -= 1
        elif c == "^":
            dy += 1
        elif c == "v":
            dy -= 1

        if santa == 0:
            x1 += dx
            y1 += dy
        else:
            x2 += dx
            y2 += dy

        santa = (santa + 1) % 2

        if not (x1, y1) in houses:
            seen += 1
            houses[(x1, y1)] = 1
        if not (x2, y2) in houses:
            seen += 1
            houses[(x2, y2)] = 1

    return seen

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

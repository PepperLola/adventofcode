import sys
import time

# shared variables here
def fully_contains(t1, t2):
    if t1[0] <= t2[0] and t1[1] >= t2[1]:
        return True
    elif (t2[0] <= t1[0]) and (t2[1] >= t1[1]):
        return True
    return False

def overlap(t1, t2):
    if t1[0] <= t2[0] <= t1[1]:
        return True
    elif t2[0] <= t1[0] <= t2[1]:
        return True
    return False

# part 1, takes in lines of file
def p1(lines):
    count = 0
    for line in lines:
        if line == "\n":
            continue
        s = line.replace("\n","").split(",")
        range1 = s[0].split("-")
        range2 = s[1].split("-")
        tuple1 = tuple([int(i) for i in range1])
        tuple2 = tuple([int(i) for i in range2])
        if fully_contains(tuple1, tuple2):
            count += 1
    return count

# part 2, takes in lines of file
def p2(lines):
    count = 0
    for line in lines:
        if line == "\n":
            continue
        s = line.replace("\n","").split(",")
        range1 = s[0].split("-")
        range2 = s[1].split("-")
        tuple1 = tuple([int(i) for i in range1])
        tuple2 = tuple([int(i) for i in range2])
        if overlap(tuple1, tuple2):
            count += 1
    return count

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

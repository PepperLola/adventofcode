import sys
import time
import re

# shared variables here
alphabet = "abcdefghijklmnopqrstuvwxyz"

def validate(pw):
    if "i" in pw or "l" in pw or "o" in pw:
        return False
    doubles = re.findall(r"(\w)\1+", pw)
    more_than_double = re.findall(r"(\w)\1{2,}", pw)
    unique_count = len(set(doubles) - set(more_than_double))
    if unique_count <= 1:
        return False
    for i in range(len(pw) - 2):
        three = pw[i:i+3]
        i1, i2, i3 = alphabet.index(three[0]), alphabet.index(three[1]), alphabet.index(three[2])
        if i2 - i1 == 1 and i3 - i2 == 1:
            return True
    return False

def propagate_increment(pw):
    if len(pw) == 1:
        return alphabet[(alphabet.index(pw) + 1) % len(alphabet)]

    last = alphabet.index(pw[-1])
    if last + 1 >= len(alphabet):
        return propagate_increment(pw[:-1]) + alphabet[(last + 1) % len(alphabet)]

    # print(pw, pw[:-1], pw[-1], last, len(alphabet))
    return pw[:-1] + propagate_increment(pw[-1])

# part 1, takes in lines of file
def p1(lines):
    line = lines[0].strip()
    valid = validate(line)
    while not valid:
        line = propagate_increment(line)
        valid = validate(line)
        # print(line, valid)

    return line

# part 2, takes in lines of file
def p2(line):
    line = propagate_increment(line)
    valid = validate(line)
    while not valid:
        line = propagate_increment(line)
        valid = validate(line)
    return line

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
    a = p2(a)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

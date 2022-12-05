import sys
import time
import re

# shared variables here
def has_double_letters(s):
    last_c = s[0]
    for c in s[1:]:
        if c == last_c:
            return True
        else:
            last_c = c

def is_nice_1(s):
    f1 = len(re.findall("[aeiou]", s)) >= 3
    f2 = has_double_letters(s)
    f3 = "ab" not in s and "cd" not in s and "pq" not in s and "xy" not in s
    return f1 and f2 and f3

# part 1, takes in lines of file
def p1(lines):
    nice = 0
    for line in lines:
        if is_nice_1(line):
            nice += 1
    return nice

def is_nice_2(s):
    doubles = {}
    has_double = len(re.findall("([a-z][a-z]).*\\1", s)) > 0

    has_repeat = len(re.findall("([a-z]).{0}[a-z]\\1", s)) > 0
    return has_double and has_repeat

# part 2, takes in lines of file
def p2(lines):
    nice = 0
    for line in lines:
        if is_nice_2(line):
            nice += 1
    return nice

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

import sys
import time
import re
import itertools
import numpy as np

# shared variables here
def is_abba(s):
    return len(s) == 4 and s == s[::-1] and s[0] != s[1]

def supports_tls(ip):
    in_brackets = False
    abba_found = False
    for i in range(len(ip)):
        if ip[i] == "[":
            in_brackets = True
            continue
        elif ip[i] == "]":
            in_brackets = False
            continue
        else:
            if is_abba(ip[i:i+4]):
                if in_brackets:
                    return False
                else:
                    abba_found = True
    return abba_found

def is_aba(aba):
    return len(aba) == 3 and aba[0] != aba[1] and aba[0] == aba[2]

def supports_ssl(ip):
    in_brackets = False
    abas = set()
    babs = set()
    for _ in range(2):
        for i in range(len(ip) - 2):
            if ip[i] == "[":
                in_brackets = True
                continue
            elif ip[i] == "]":
                in_brackets = False
                continue
            else:
                aba = ip[i:i+3]
                if is_aba(aba):
                    if in_brackets:
                        if aba[1] + aba[0] + aba[1] in abas:
                            return True
                    else:
                        abas.add(aba)

# part 1, takes in lines of file
def p1(lines):
    c = 0
    for line in lines:
        line = line.strip()
        if supports_tls(line):
            c += 1
    return c


# part 2, takes in lines of file
def p2(lines):
    c = 0
    for line in lines:
        line = line.strip()
        if supports_ssl(line):
            c += 1
    return c

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

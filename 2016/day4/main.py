import sys
import time
import re
import itertools
import numpy as np

# shared variables here
def most_common_letters(s):
    letters = {}
    for c in s:
        if not c in letters:
            letters[c] = 1
        else:
            letters[c] += 1

    # reverse
    reversed_letters = {}
    for key in letters.keys():
        if not letters[key] in reversed_letters:
            reversed_letters[letters[key]] = [key]
        else:
            reversed_letters[letters[key]].append(key)

    sorted_frequencies = sorted(list(reversed_letters.keys()), reverse=True)
    most_common = []
    for key in sorted_frequencies:
        most_common += sorted(reversed_letters[key])
    return most_common

alphabet = "abcdefghijklmnopqrstuvwxyz"
def shift_name(s, shift):
    words = s.split("-")
    res = []
    for word in words:
        word_split = list(word)
        for i in range(len(word_split)):
            word_split[i] = alphabet[(alphabet.index(word[i]) + shift) % len(alphabet)] 
        # print(word, word_split)
        res.append("".join(word_split))

    # print(res)
    return " ".join(res)

real_rooms = []

# part 1, takes in lines of file
def p1(lines):
    real = 0
    for line in lines:
        line = line.strip()
        m = re.search("((?:\w+-)*)(\d+)\[(\w+)\]", line)
        if m:
            name = m.group(1).replace("-", "")
            if "".join(most_common_letters(name)[:5]) == m.group(3):
                sector = int(m.group(2))
                real_rooms.append((m.group(1)[:-1], sector))
                real += sector
    return real

# part 2, takes in lines of file
def p2(lines):
    real = 0
    for i in range(len(real_rooms)):
        room = real_rooms[i]
        for shift in range(26):
            shifted = shift_name(room[0], shift)
            if "north" in shifted.lower():
                return room[1]
    return real

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

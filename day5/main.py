import sys
import time
import re

# shared variables here

# part 1, takes in lines of file
def p1(lines):
    crates = []
    for line in lines:
        if '[' in line:
            last_idx = 0
            while last_idx != -1:
                if not "[" in line[last_idx + 1:]:
                    break
                last_idx = line.index("[", last_idx)
                i = last_idx // 4
                while len(crates) < i + 1:
                    crates.append([])
                crates[i].append(line[last_idx + 1])
                last_idx += 1
        elif line != "\n" and "move" in line:
            moves = re.findall("[0-9]+", line)
            amt = int(moves[0])
            chosen_crate = int(moves[1]) - 1
            dest_crate = int(moves[2]) - 1
            temp = []
            # print(line, crates[chosen_crate], crates[dest_crate], amt)
            for i in range(amt):
                crates[dest_crate] = [crates[chosen_crate][0]] + crates[dest_crate]
                crates[chosen_crate] = crates[chosen_crate][1:]
                
    res = ""
    for stack in crates:
        res += stack[0]
    return res

# part 2, takes in lines of file
def p2(lines):
    crates = []
    for line in lines:
        if '[' in line:
            last_idx = 0
            while last_idx != -1:
                if not "[" in line[last_idx + 1:]:
                    break
                last_idx = line.index("[", last_idx)
                i = last_idx // 4
                while len(crates) < i + 1:
                    crates.append([])
                crates[i].append(line[last_idx + 1])
                last_idx += 1
        elif line != "\n" and "move" in line:
            moves = re.findall("[0-9]+", line)
            amt = int(moves[0])
            chosen_crate = int(moves[1]) - 1
            dest_crate = int(moves[2]) - 1
            temp = []
            # print(line, crates[chosen_crate], crates[dest_crate], amt)
            for i in range(amt):
                temp.append(crates[chosen_crate][0])
                crates[chosen_crate] = crates[chosen_crate][1:]
            crates[dest_crate] = temp + crates[dest_crate]
                
    res = ""
    for stack in crates:
        res += stack[0]
    return res

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

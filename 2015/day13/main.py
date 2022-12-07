import sys
import time
import re
import itertools

# shared variables here
people = {}
happinesses = {}

# part 1, takes in lines of file
def p1(lines):
    for line in lines:
        match = re.search(r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).", line)
        if match:
            person = match.group(1)
            mult = 1 if match.group(2) == "gain" else -1
            happiness = int(match.group(3))
            partner = match.group(4)
            if person not in people:
                people[person] = {}
            people[person][partner] = happiness * mult

    perms = itertools.permutations(list(people.keys()))
    for perm in perms:
        happiness = 0
        for i in range(len(perm)):
            person = perm[i]
            happiness += people[person][perm[(i + 1) % len(people)]]
            happiness += people[person][perm[(i - 1 + len(people) % len(people))]]
        happinesses[happiness] = perm

    max_happiness = max(happinesses.keys())
    return max_happiness

# part 2, takes in lines of file
def p2(lines):
    people_list = list(people.keys())
    people['Me'] = {}
    for person in people_list:
        people['Me'][person] = 0
        people[person]['Me'] = 0

    perms = itertools.permutations(list(people.keys()))
    happinesses = {}
    for perm in perms:
        happiness = 0
        for i in range(len(perm)):
            person = perm[i]
            happiness += people[person][perm[(i + 1) % len(people)]]
            happiness += people[person][perm[(i - 1 + len(people) % len(people))]]
        happinesses[happiness] = perm

    max_happiness = max(happinesses.keys())

    return max_happiness

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

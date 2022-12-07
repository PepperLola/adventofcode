import sys
import time
import re
from collections import namedtuple

class Reindeer:
    def __init__(self, name, velocity, fly_dur, rest, state, state_time, distance, points):
        self.name = name
        self.velocity = velocity
        self.fly_dur = fly_dur
        self.rest = rest
        self.state = state
        self.state_time = state_time
        self.distance = distance
        self.points = points

# state: False = resting, True = flying
# state_time: time in state

# shared variables here
TIME = 2503

# part 1, takes in lines of file
def p1(lines):
    reindeers = []
    for line in lines:
        match = re.search("(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.", line)
        if match:
            reindeers.append(Reindeer(match.group(1), int(match.group(2)), int(match.group(3)), int(match.group(4)), True, 0, 0, 0))

    for s in range(TIME):
        for reindeer in reindeers:
            reindeer.state_time += 1
            if reindeer.state:
                reindeer.distance += reindeer.velocity
            if reindeer.state and reindeer.state_time >= reindeer.fly_dur:
                reindeer.state = False
                reindeer.state_time = 0
            elif not reindeer.state and reindeer.state_time >= reindeer.rest:
                reindeer.state = True
                reindeer.state_time = 0

    return max([r.distance for r in reindeers])

# part 2, takes in lines of file
def p2(lines):
    reindeers = []
    for line in lines:
        match = re.search("(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.", line)
        if match:
            reindeers.append(Reindeer(match.group(1), int(match.group(2)), int(match.group(3)), int(match.group(4)), True, 0, 0, 0))

    for s in range(TIME):
        for reindeer in reindeers:
            reindeer.state_time += 1
            if reindeer.state:
                reindeer.distance += reindeer.velocity
            if reindeer.state and reindeer.state_time >= reindeer.fly_dur:
                reindeer.state = False
                reindeer.state_time = 0
            elif not reindeer.state and reindeer.state_time >= reindeer.rest:
                reindeer.state = True
                reindeer.state_time = 0
        reindeers.sort(key=lambda r: r.distance, reverse=True)
        reindeers[0].points += 1

    return max([r.points for r in reindeers])

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

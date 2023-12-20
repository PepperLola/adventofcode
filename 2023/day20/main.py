import sys
import time
import re
import itertools
from itertools import count
from collections import defaultdict, deque
import math
import copy
from typing import Deque
import numpy as np
from util import format_time, number_grid

# shared variables here
def sum_pulses(prev, new):
    ret = [x+y for x, y in zip(prev, new)]
    return ret

def send_pulse(pulse, name, prev_name, modules):
    # low, high
    pulses = [0, 1] if pulse == 1 else [1, 0]
    if name not in modules.keys():
        return [0, 0]
    module = modules[name]
    dest = module["dest"]
    if module["type"] == "%" and pulse == 0:
        module["state"] = 1 if module["state"] == 0 else 0
        for d in dest:
            print(f"{name} -{['low', 'high'][module['state']]}-> {d}")
            pulses = sum_pulses(pulses, send_pulse(module["state"], d, name, modules))
    elif module["type"] == "&":
        module["ins"] = list(filter(lambda x: x[0] != prev_name, module["ins"]))
        module["ins"].append((prev_name, pulse))
        all_high = True
        for ps in module["ins"]:
            if ps[1] == 0:
                all_high = False
                break
        for d in dest:
            print(f"{name} -{['low', 'high'][0 if all_high else 1]}-> {d}")
            pulses = sum_pulses(pulses, send_pulse(0 if all_high else 1, d, name, modules))
    elif module["type"] == "broadcaster":
        for d in dest:
            print(f"{name} -low-> {d}")
            pulses = sum_pulses(pulses, send_pulse(pulse, d, name, modules))

    return pulses

# part 1, takes in lines of file
def p1(file, content, lines):
    modules = {}
    for line in lines:
        s = line.split(" -> ")
        name = s[0]
        t = "broadcaster"
        if name != "broadcaster":
            t, name = name[0], name[1:]
            modules[name] = {"type": t, "dest": s[1].split(", "), "state": 0, "ins": []}
        else:
            modules[name] = {"type": "broadcaster", "dest": s[1].split(", ")}
    for name, data in modules.items():
        dests = data["dest"]
        for d in dests:
            if d not in modules.keys():
                continue
            if modules[d]["type"] == "&":
                modules[d]["ins"].append([ name, 0 ])
    
    total = [0, 0]
    for i in range(1000):
        total[0] += 1
        # print("button -low-> broadcaster")
        q: Deque[tuple[str, str, int]] = deque([("broadcaster", "", 0)])
        while len(q) > 0:
            name, prev, pulse = q.popleft()
            if name not in modules.keys():
                continue
            module = modules[name]
            dest = module["dest"]
            if module["type"] == "%" and pulse == 0:
                module["state"] = 1 if module["state"] == 0 else 0
                for d in dest:
                    # print(f"{name} -{['low', 'high'][module['state']]}-> {d}")
                    total[module["state"]] += 1
                    q.append((d, name, module["state"]))
            elif module["type"] == "&":
                module["ins"] = list(filter(lambda x: x[0] != prev, module["ins"]))
                module["ins"].append((prev, pulse))
                all_high = True
                for ps in module["ins"]:
                    if ps[1] == 0:
                        all_high = False
                        break
                # print(name, module["ins"], prev, pulse)
                for d in dest:
                    # print(f"{name} -{['low', 'high'][0 if all_high else 1]}-> {d}")
                    total[0 if all_high else 1] += 1
                    q.append((d, name, 0 if all_high else 1))
            elif module["type"] == "broadcaster":
                for d in dest:
                    # print(f"{name} -low-> {d}")
                    total[pulse] += 1
                    q.append((d, name, pulse))
        # print('---')
    return np.prod(total)
    

# part 2, takes in lines of file
def p2(file, content, lines):
    modules = {}
    lead_to_rx = None
    for line in lines:
        s = line.split(" -> ")
        name = s[0]
        t = "broadcaster"
        if name != "broadcaster":
            t, name = name[0], name[1:]
            modules[name] = {"type": t, "dest": s[1].split(", "), "state": 0, "ins": []}
        else:
            modules[name] = {"type": "broadcaster", "dest": s[1].split(", ")}
    for name, data in modules.items():
        dests = data["dest"]
        if "rx" in dests:
            lead_to_rx = name
        for d in dests:
            if d not in modules.keys():
                continue
            if modules[d]["type"] == "&":
                modules[d]["ins"].append([ name, 0 ])

    to_rx = list(map(lambda x: x[0], filter(lambda x: lead_to_rx in x[1]["dest"], modules.items())))
    to_lcm = {}
    prev_i = {}
    counts = {name: 0 for name in to_rx}
    for i in count(1):
        q: Deque[tuple[str, str, int]] = deque([("broadcaster", "", 0)])
        while len(q) > 0:
            name, prev, pulse = q.popleft()
            if len(to_lcm.keys()) == len(to_rx):
                return math.lcm(*to_lcm.values())
            elif name in to_rx and pulse == 0:
                counts[name] += 1
                if counts[name] == 2:
                    to_lcm[name] = i - prev_i[name]
                else:
                    prev_i[name] = i
            if name not in modules.keys():
                continue
            module = modules[name]
            dest = module["dest"]
            if module["type"] == "%" and pulse == 0:
                module["state"] = 1 if module["state"] == 0 else 0
                for d in dest:
                    q.append((d, name, module["state"]))
            elif module["type"] == "&":
                module["ins"] = list(filter(lambda x: x[0] != prev, module["ins"]))
                module["ins"].append((prev, pulse))
                all_high = True
                for ps in module["ins"]:
                    if ps[1] == 0:
                        all_high = False
                        break
                for d in dest:
                    q.append((d, name, 0 if all_high else 1))
            elif module["type"] == "broadcaster":
                for d in dest:
                    q.append((d, name, pulse))
    return -1

filename = "input.txt"

if "test" in sys.argv:
    filename = "test.txt"

with open(filename, "r") as f:
    content = f.read()
    lines = content.splitlines()
    t = time.perf_counter_ns()
    a = p1(f, content, lines)
    dur = time.perf_counter_ns() - t

    print("\033[0;33m├ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

    t = time.perf_counter_ns()
    a = p2(f, content, lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 2:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

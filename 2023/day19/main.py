import sys
import time
import re
import itertools
import json
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid

# shared variables here
p = re.compile(r"(\w+)\{(.+)\}$")
workflows = {}

def pred_fn(item, vn, op, val):
    return item[vn] < int(val) if op == "<" else item[vn] > int(val)

max_rating = 4000

def parts():
    for i in range(max_rating * max_rating * max_rating):
        print(i)
        yield {
                "x": max(1, i % max_rating),
                "m": max(1, i // max_rating % max_rating),
                "a": max(1, i // (max_rating * max_rating) % max_rating),
                "s": max(1, i // (max_rating * max_rating * max_rating) % max_rating)
       }

# part 1, takes in lines of file
def p1(file, content, lines):
    global workflows
    items = []
    parsing_items = False
    for line in lines:
        if line.strip() == "":
            parsing_items = True
        else:
            if parsing_items:
                line = line[1:-1]
                item = {}
                for a in line.split(","):
                    vn, val = a.split("=")
                    item[vn] = int(val)
                items.append(item)
            else:
                m = p.match(line.strip())
                if m is None:
                    continue
                wname = m.group(1)
                data = m.group(2)
                s = data.split(",")
                preds = []
                for pred in s:
                    if not ":" in pred:
                        preds.append(pred)
                        continue
                    cond, res = pred.split(":")
                    vn, op, val = cond[0], cond[1], int(cond[2:])
                    preds.append((vn, op, val, res))
                workflow = {"name": wname, "predicates": preds}
                workflows[wname] = workflow
    result = {'A': [], 'R': []}
    for item in items:
        wflow_name = 'in'
        while not wflow_name in "RA":
            wflow = workflows[wflow_name]
            for pred in wflow['predicates']:
                if str(pred) == pred:
                    wflow_name = pred
                    continue
                valid = pred_fn(item, *pred[:3])
                if valid:
                    wflow_name = pred[-1]
                    break
        result[wflow_name].append(item)
    return sum(map(lambda item: sum(item.values()), result["A"]))

def next_ranges(ch, gt, val, ranges):
	ch = 'xmas'.index(ch)
	ranges2 = []
	for rng in ranges:
		rng = list(rng)
		lo, hi = rng[ch]
		if gt:
			lo = max(lo, val + 1)
		else:
			hi = min(hi, val - 1)
		if lo > hi:
			continue
		rng[ch] = (lo, hi)
		ranges2.append(tuple(rng))
	return ranges2

A_RET = [((1, 4000), (1, 4000), (1, 4000), (1, 4000))]
R_RET = []

def valid_ranges(w, workflow):
    if str(w) == w:
        return valid_ranges(workflow[w], workflow)
    it = w[0]
    if it == "R":
        return []
    if it == "A":
        return [((1, 4000), (1, 4000), (1, 4000), (1, 4000))]
    if ":" not in it:
        return valid_ranges(it, workflow)
    cond = it.split(":")[0]
    gt = ">" in cond
    ch = cond[0]
    val = int(cond[2:])
    if_true = next_ranges(ch, gt, val, valid_ranges([it.split(":")[1]], workflow))
    if_false = next_ranges(ch, not gt, val + 1 if gt else val - 1, valid_ranges(w[1:], workflow))
    return if_true + if_false

# part 2, takes in lines of file
def p2(file, content, lines):
    total = 0
    global workflows

    workflows = {}

    for line in lines:
        if line.strip() == "":
            break
        m = p.match(line)
        if m is None:
            continue
        workflows[m.group(1)] = m.group(2).split(",")

    for rng in valid_ranges('in', workflows):
        valid = 1
        for minv, maxv in rng:
            valid *= maxv - minv + 1
        total += valid
        
    return total

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

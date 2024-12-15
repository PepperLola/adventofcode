import sys
import time
import re
import itertools
from collections import defaultdict, deque, Counter
import math
import copy
import numpy as np
import networkx as nx
from util import format_time, number_grid

# shared variables here
walls = set()
boxes = set()
robot = (-1, -1)
dirs = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1)
}

def try_push_box_1(box, dir):
    global walls, boxes, robot
    bx, by = box
    dx, dy = dir
    new_box = (dx + bx, dy + by)
    if not new_box in walls and not new_box in boxes:
        robot = box
        boxes.remove(box)
        boxes.add(new_box)
        return True
    elif not new_box in boxes and new_box in walls:
        return False
    else:
        if try_push_box_1(new_box, dir):
            robot = box
            boxes.remove(box)
            boxes.add(new_box)
            return True
    return False

def try_push_box_2(pos, dir):
    global walls, boxes, robot
    box = find_box(pos)
    if box == None:
        return False
    (bx1, by1), (bx2, by2) = box
    dx, dy = dir
    new_box_1 = (dx + bx1, dy + by1)
    new_box_2 = (dx + bx2, dy + by2)
    nb = (new_box_1, new_box_2)
    if dy != 0:
        # could push multiple
        if not new_box_1 in walls and not new_box_2 in walls and not has_box(new_box_1) and not has_box(new_box_2):
            robot = pos
            boxes.remove(box)
            boxes.add(nb)
            return True
        elif new_box_1 in walls or new_box_2 in walls:
            return False
        else:
            old_boxes = copy.deepcopy(boxes)
            old_robot = copy.deepcopy(robot)
            if nb in boxes:
                if try_push_box_2(new_box_1, dir):
                    robot = pos
                    boxes.remove(box)
                    boxes.add(nb)
                    return True
                return False

            succeeded_1 = True
            if has_box(new_box_1):
                succeeded_1 = try_push_box_2(new_box_1, dir)
            if not succeeded_1:
                return False
            if not has_box(new_box_2) or try_push_box_2(new_box_2, dir):
                robot = pos
                boxes.remove(box)
                boxes.add(nb)
                return True
            else:
                boxes = old_boxes
                robot = old_robot
    else:
        # can only push one
        if not new_box_1 in walls and not new_box_2 in walls and ((dx < 0 and not has_box(new_box_1)) or (dx > 0 and not has_box(new_box_2))):
            robot = pos
            boxes.remove(box)
            boxes.add(nb)
            return True
        elif new_box_1 in walls:
            return False
        else:
            if try_push_box_2(new_box_1 if dx < 0 else new_box_2, dir):
                robot = pos
                boxes.remove(box)
                boxes.add(nb)
                return True
    return False

# part 1, takes in lines of file
def p1(file, content, lines):
    global walls, boxes, robot, dirs
    blank_line = 0
    for y, line in enumerate(lines):
        if line == "":
            blank_line = y
            break
        for x, c in enumerate(line):
            if c == "#":
                walls.add((x, y))
            elif c == "O":
                boxes.add((x, y))
            elif c == "@":
                robot = (x, y)
    inst = "".join(lines[blank_line:])
    for c in inst:
        dx, dy = dirs[c]
        rx, ry = robot
        new_pos = (dx + rx, dy + ry)
        if not new_pos in walls and not new_pos in boxes:
            robot = new_pos
        elif new_pos in boxes:
            try_push_box_1(new_pos, dirs[c])
    ret = 0
    for bx, by in boxes:
        ret += 100 * by + bx
    return ret

def has_box(pos):
    global boxes
    x, y = pos
    return ((x, y), (x+1, y)) in boxes or ((x-1, y), (x, y)) in boxes

def find_box(pos):
    global boxes
    x, y = pos
    if ((x, y), (x+1, y)) in boxes:
        return ((x, y), (x+1, y))
    elif ((x-1, y), (x, y)) in boxes:
        return ((x-1, y), (x, y))
    return None

# part 2, takes in lines of file
def p2(file, content, lines):
    global walls, boxes, robot, dirs
    walls.clear()
    boxes.clear()
    blank_line = 0
    for y, line in enumerate(lines):
        if line == "":
            blank_line = y
            break
        for x, c in enumerate(line):
            if c == "#":
                walls.add((x*2, y))
                walls.add((x*2+1, y))
            elif c == "O":
                boxes.add(((x*2, y), (x*2+1, y)))
            elif c == "@":
                robot = (x*2, y)
    inst = "".join(lines[blank_line:])
    for c in inst:
        dx, dy = dirs[c]
        rx, ry = robot
        new_pos = (dx + rx, dy + ry)
        if not new_pos in walls and not has_box(new_pos):
            robot = new_pos
        elif has_box(new_pos):
            try_push_box_2(new_pos, dirs[c])
    ret = 0
    for (bx, by), (_, _) in boxes:
        ret += 100 * by + bx
    return ret

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

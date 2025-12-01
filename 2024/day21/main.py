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
from functools import cache

# shared variables here

positions = {
    '9': (2, 0),
    '8': (1, 0),
    '7': (0, 0),
    '6': (2, 1),
    '5': (1, 1),
    '4': (0, 1),
    '3': (2, 2),
    '2': (1, 2),
    '1': (0, 2),
    'A': (2, 3),
    '0': (1, 3)
}

positions_dir = {
    'A': (2, 0),
    '^': (1, 0),
    '>': (2, 1),
    'v': (1, 1),
    '<': (0, 1)
}

def complexity(code, seq):
    print(code, len(seq))
    return len(seq) * int("".join(list(filter(lambda x: x.isdigit(), list(code)))))

def to_next_alpha(next, start=(2, 3)):
    tx, ty = next
    sx, sy = start
    dx, dy = tx-sx, ty-sy

    return ['', '>', '<'][np.sign(dx)]*abs(dx) + ['', 'v', '^'][np.sign(dy)]*abs(dy)

def to_next_dir(next, start=(2, 0)):
    tx, ty = next
    sx, sy = start
    dx, dy = tx-sx, ty-sy

    return ['', '>', '<'][np.sign(dx)]*abs(dx) + ['', 'v', '^'][np.sign(dy)]*abs(dy)

gn = nx.Graph()

gn.add_node(positions["A"])
gn.add_node(positions["0"])
gn.add_node(positions["1"])
gn.add_node(positions["2"])
gn.add_node(positions["3"])
gn.add_node(positions["4"])
gn.add_node(positions["5"])
gn.add_node(positions["6"])
gn.add_node(positions["7"])
gn.add_node(positions["8"])
gn.add_node(positions["9"])

gn.add_edge(positions["A"], positions["0"])
gn.add_edge(positions["A"], positions["3"])
gn.add_edge(positions["0"], positions["2"])
gn.add_edge(positions["1"], positions["4"])
gn.add_edge(positions["2"], positions["1"])
gn.add_edge(positions["2"], positions["5"])
gn.add_edge(positions["2"], positions["3"])
gn.add_edge(positions["3"], positions["6"])
gn.add_edge(positions["4"], positions["7"])
gn.add_edge(positions["4"], positions["5"])
gn.add_edge(positions["5"], positions["8"])
gn.add_edge(positions["5"], positions["6"])
gn.add_edge(positions["6"], positions["9"])
gn.add_edge(positions["7"], positions["8"])
gn.add_edge(positions["8"], positions["9"])


gd = nx.Graph()
gd.add_node(positions_dir["^"])
gd.add_node(positions_dir["<"])
gd.add_node(positions_dir["v"])
gd.add_node(positions_dir[">"])

gd.add_edge(positions_dir["A"], positions_dir["^"])
gd.add_edge(positions_dir["A"], positions_dir[">"])
gd.add_edge(positions_dir["^"], positions_dir["v"])
gd.add_edge(positions_dir["<"], positions_dir["v"])
gd.add_edge(positions_dir["v"], positions_dir[">"])

def dist(pt1, pt2):
    (x1, y1), (x2, y2) = (pt1, pt2)
    return abs(x2-x1) + abs(y2-y1)

def sort_moves(moves, start, pos):
    if len(moves) == 0:
        return ""
    mov_map = list(map(lambda x: (x[0], dist(pos[start], pos[x[0]])), moves))
    # print(mov_map)
    mov_map = sorted(mov_map, key=lambda x: x[1])

    # print(mov_map[0][0])

    return mov_map[0][0] + sort_moves(
        list(map(lambda x: x[0], mov_map[1:])),
        mov_map[0][0],
        pos
    )

@cache
def shortest(moves, on_alpha=True, limit=2, depth=0):
    global positions_dir, positions
    pos = positions if on_alpha else positions_dir
    print(on_alpha)
    s = pos["A"]
    ret = 0
    for b in list(moves):
        print(s, b)
        pls = nx.shortest_simple_paths(gn if on_alpha else gd, source=s, target=b)
        if depth >= limit:
            ret += len(min(pls, key=len))
        else:
            min_moves = float('inf')
            for pl in pls:
                print(pl)
                # TODO: pass in character instead of coord for later graph
                new_len = shortest(tuple(pl), False, limit, depth+1)
                min_moves = min(min_moves, new_len)
            if min_moves == float('inf'):
                ret += len(min(pls, key=len))
            else:
                ret += min_moves
        s = b
    return ret


# part 1, takes in lines of file
def p1(file, content, lines):
    ret = 0
    for line in lines:
        final_moves = shortest(tuple(map(lambda x: positions[x], line)))
    return ret

# part 2, takes in lines of file
def p2(file, content, lines):
    return 0

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

import sys
import time
import re
import itertools
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import math
import copy
import numpy as np
import networkx as nx
from util import format_time, number_grid

# shared variables here
def test_two_parts(pairs, to_remove):
    new_pairs = [p for p in pairs if p not in to_remove]
    

# part 1, takes in lines of file
def p1(file, content, lines):
    g = nx.Graph()
    for line in lines:
        src, rest = line.split(": ")
        dests = rest.split(" ")
        pairs = zip([src] * len(dests), dests)
        for pair in pairs:
            g.add_edge(pair[0], pair[1])
    cuts = nx.minimum_edge_cut(g)
    g.remove_edges_from(cuts)
    # nx.draw_networkx(g)
    # plt.show()
    return np.prod(list(map(len, nx.connected_components(g))))

filename = "input.txt"

if "test" in sys.argv:
    filename = "test.txt"

with open(filename, "r") as f:
    content = f.read()
    lines = content.splitlines()

    t = time.perf_counter_ns()
    a = p1(f, content, lines)
    dur = time.perf_counter_ns() - t
    print("\033[0;33m└ Part 1:\033[22m\033[49m \033[1;93m%s\033[0m \033[3mtook\033[23m \033[3;92m%s\033[0m" % (a, format_time(dur)))

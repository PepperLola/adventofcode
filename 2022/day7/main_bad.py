import sys
import time
import re
import itertools
from treelib import Node, Tree

# shared variables here
tree = Tree()
size = 0

def calculate_size(node):
    if " " in node:
        match = re.search(r"(\d+) (.*)", node)
        if match:
            return int(match.group(1))
    node_size = 0
    subtree = tree.children(node)
    for subnode in subtree:
        node_size += calculate_size(subnode.identifier)

    return node_size

# part 1, takes in lines of file
def p1(lines):
    total = 0
    current_node = None
    for line in lines:
        if "$" in line:
            if "cd" in line:
                match = re.search("cd (.*)$", line)
                if match:
                    name = match.group(1)
                    if name == "..":
                        parent = tree.parent(current_node.identifier)
                        if parent != None:
                            current_node = tree.parent(current_node.identifier)
                    else:
                        identifier = f"{current_node.tag + '-' if current_node != None else ''}{name}"
                        if tree.contains(identifier):
                            current_node = tree.get_node(identifier)
                        else:
                            current_node = tree.create_node(name, f"{current_node.tag + '-' if current_node != None else ''}{name}", parent=current_node)

        else:
            # if "dir" in line:
                # match = re.search("dir (\w+)", line)
                # if match:
                    # if not tree.contains(match.group(1)):
                        # tree.create_node(match.group(1), parent=current_node.identifier)
            # else:
            match = re.search(r"(\d+) (.*)", line)
            if match:
                tree.create_node(match.group(0), f"{current_node.tag}-{match.group(0)}", parent=current_node.identifier)

    tree.show(idhidden=False)

    nodes = [(node, calculate_size(node)) for node in tree.expand_tree(mode=Tree.DEPTH) if not " " in node]
    filtered = tree.filter_nodes(lambda node: calculate_size(node) < 100000)
    nodes = [node[1] for node in nodes if node[1] < 100000]
    print(filtered)

    # print(nodes)

    # for node in [tree[node].tag for node in tree.expand_tree(mode=Tree.DEPTH) if not re.search(r"\d", node)]:
        # print(node)
        # size = calculate_size(node)
        # if size <= 100000:
            # total += size

    return sum(nodes)

# part 2, takes in lines of file
def p2(lines):
    return 0

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

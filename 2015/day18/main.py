import sys
import time
import re
import numpy as np
import copy

# shared variables here
def format_board(board):
    s = ""
    for line in board:
        for c in line:
            if c == True:
                s += "#"
            else:
                s += "."
        s += "\n"
    return s

def process_iteration(board):
    new_board = copy.deepcopy(board)
    for y in range(len(board)):
        for x in range(len(board[0])):
            neighbors = sum_of_neighbors(board, x, y)
            if neighbors == 3:
                new_board[y][x] = True
            elif neighbors != 2:
                new_board[y][x] = False
    return new_board
    
def sum_of_neighbors(board, x, y):
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            if x + dx >= 0 and x + dx < len(board[0]):
                if y + dy >= 0 and y + dy < len(board):
                    # print("X", x, "Y", y, "VAL", board[y][x], "+dx", x + dx, "+dy", y + dy, "OTHER", board[y+dy][x+dx])
                    if board[y+dy][x+dx] == True:
                        count += 1
    return count

def set_corners(board):
    board[0][0] = True
    board[len(board) - 1][0] = True
    board[0][len(board[0]) - 1] = True
    board[len(board) - 1][len(board[0]) - 1] = True
    return board

# part 1, takes in lines of file
def p1(lines):
    lines = [line.strip() for line in lines if line != "\n"]
    board = np.zeros((len(lines[0]), len(lines)))
    for y in range(len(lines)):
        for x in range(len(lines[y].strip())):
            c = lines[y].strip()[x]
            if c == "#":
                board[y][x] = True
            else:
                board[y][x] = False

    STEPS = 100
    for gen in range(STEPS):
        board = process_iteration(board)
    return sum(sum(board))

# part 2, takes in lines of file
def p2(lines):
    lines = [line.strip() for line in lines if line != "\n"]
    board = np.zeros((len(lines[0]), len(lines)))
    for y in range(len(lines)):
        for x in range(len(lines[y].strip())):
            c = lines[y].strip()[x]
            if c == "#":
                board[y][x] = True
            else:
                board[y][x] = False

    STEPS = 100
    board = set_corners(board)
    for gen in range(STEPS):
        board = process_iteration(board)
        board = set_corners(board)
        # print(format_board(board))
    return sum(sum(board))


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

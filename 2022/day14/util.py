import numpy as np

alphabet = "abcdefghijklmnopqrstuvwxyz"

def letter_grid(file, separator = ""):
    lines = file.read().splitlines()
    grid = [['' for x in range(len(lines[0]))] for y in range(len(lines))]
    for y in range(len(lines)):
        line = list(lines[y]) if separator == "" else lines[y].split(separator)
        for x in range(len(line)):
            grid[y][x] = line[x]
    return grid

def number_grid(file, separator = ""):
    lines = file.read().splitlines()
    grid = np.zeros((len(lines), len(lines[0])))
    for y in range(len(lines)):
        line = list(lines[y]) if separator == "" else lines[y].split(separator)
        for x in range(len(line)):
            grid[y][x] = int(line[x])
    return grid

def alphabet_scale_grid(file, separator=""):
    global alphabet
    grid = letter_grid(file, separator)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in alphabet:
                grid[y][x] = alphabet.index(grid[y][x])
    return grid

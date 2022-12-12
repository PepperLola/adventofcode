import numpy as np

def letter_grid(file, separator = ""):
    lines = file.read().splitlines()
    grid = [['' for x in range(len(lines[0]))] for y in range(len(lines))]
    for y in range(len(lines)):
        line = lines[y].split() if separator == "" else lines[y].split(separator)
        for x in range(len(line)):
            grid[y][x] = line[x]
    return grid

def number_grid(file, separator = ""):
    lines = file.read().splitlines()
    grid = np.zeros((len(lines), len(lines[0])))
    for y in range(len(lines)):
        line = lines[y].split() if separator == "" else lines[y].split(separator)
        for x in range(len(line)):
            grid[y][x] = int(line[x])
    return grid

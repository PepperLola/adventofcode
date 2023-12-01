import numpy as np

alphabet = "abcdefghijklmnopqrstuvwxyz"

def letter_grid_file(file, separator = ""):
    lines = file.read().splitlines()
    return letter_grid(lines, separator)

def number_grid_file(file, separator = ""):
    lines = file.read().splitlines()
    return number_grid(lines, separator)

def alphabet_scale_grid_file(file, separator=""):
    global alphabet
    lines = file.read().splitlines()
    return alphabet_scale_grid(lines, separator)

def letter_grid(lines, separator = ""):
    first_line = lines[0].replace(separator, "")
    grid = [['' for x in range(len(first_line))] for y in range(len(lines))]
    for y in range(len(lines)):
        line = list(lines[y]) if separator == "" else lines[y].split(separator)
        for x in range(len(line)):
            grid[y][x] = line[x]
    return grid

def number_grid(lines, separator = ""):
    first_line = lines[0].replace(separator, "")
    grid = np.zeros((len(lines), len(first_line)))
    for y in range(len(lines)):
        line = list(lines[y]) if separator == "" else lines[y].split(separator)
        for x in range(len(line)):
            grid[y][x] = int(line[x])
    return grid

def alphabet_scale_grid(lines, separator = ""):
    grid = letter_grid(lines, separator)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in alphabet:
                grid[y][x] = alphabet.index(grid[y][x])
    return grid

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

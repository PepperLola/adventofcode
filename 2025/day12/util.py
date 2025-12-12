import itertools
import numpy as np
import math
import re

alphabet = "abcdefghijklmnopqrstuvwxyz"

# All 3x3 neighbor directions including diagonals
ds = itertools.product([-1, 0, 1], [-1, 0, 1])

def letter_grid_file(file, separator: str = ""):
    """
    Load a text file into a 2D grid of characters.
    """
    lines = file.read().splitlines()
    return letter_grid(lines, separator)

def number_grid_file(file, separator: str = ""):
    """
    Load a text file into a 2D numpy array of integers.
    """
    lines: list[str] = file.read().splitlines()
    return number_grid(lines, separator)

def alphabet_scale_grid_file(file, separator: str = ""):
    """
    Load a file into a 2D grid where each lowercase letter becomes its index in the alphabet (a=0, b=1, ...).
    """
    global alphabet
    lines = file.read().splitlines()
    return alphabet_scale_grid(lines, separator)

def letter_grid(lines: list[str], separator: str = ""):
    """
    Convert a list of strings into a 2D grid of characters.
    """
    first_line = lines[0].replace(separator, "")
    grid = [['' for x in range(len(first_line))] for y in range(len(lines))]
    for y in range(len(lines)):
        line = list(lines[y]) if separator == "" else lines[y].split(separator)
        for x in range(len(line)):
            grid[y][x] = line[x]
    return grid

def number_grid(lines: list[str], separator: str = ""):
    """
    Convert a list of strings into a 2D array of integers.
    """
    first_line = lines[0].replace(separator, "")
    grid = np.zeros((len(lines), len(first_line)))
    for y in range(len(lines)):
        line = list(lines[y]) if separator == "" else lines[y].split(separator)
        for x in range(len(line)):
            grid[y][x] = int(line[x])
    return grid

def alphabet_scale_grid(lines: list[str], separator: str = ""):
    """
    Convert a text grid into numbers where each lowercase letter becomes its index in the alphabet (a=0, b=1, ...).
    """
    grid = letter_grid(lines, separator)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in alphabet:
                grid[y][x] = alphabet.index(grid[y][x])
    return grid

def find_grid(grid: list[list[str]], arr):
    """
    Find the first occurrence of a 2D pattern inside a larger 2D grid.
    """
    H = len(grid)
    W = len(grid[0])
    shape = np.shape(arr)
    if len(shape) == 1:
        arr = [arr]
        shape = np.shape(arr)
    IH, IW = shape
    for row in range(H):
        for col in range(W):
            for off_row in range(IH):
                good = True
                for off_col in range(IW):
                    if arr[off_row][off_col] != None and grid[row + off_row][col + off_col] != arr[off_row][off_col]:
                        good = False
                        break
                if not good:
                    break
                return (col, row)
    return None

def find_all_grid(grid: list[list[str]], arr):
    """
    Find all occurrences of a pattern inside a 2D grid.
    """
    H = len(grid)
    W = len(grid[0])
    shape = np.shape(arr)
    if len(shape) == 1:
        arr = [arr]
        shape = np.shape(arr)
    IH, IW = shape
    ret = []
    for row in range(H - IH + 1):
        for col in range(W - IW + 1):
            good = True
            for off_row in range(IH):
                for off_col in range(IW):
                    if arr[off_row][off_col] != None and grid[row + off_row][col + off_col] != arr[off_row][off_col]:
                        good = False
                        break
                if not good:
                    break
            if good:
                ret.append((col, row))
    return ret

def parse_str_6(s: str, fg: str = "#", bg: str = " "):
    """
    Parse a 6-row ASCII art block into letters.
    """
    letters = {
        " ## \n#  #\n####\n#  #\n#  #\n#  #\n": "A",
        "### \n#  #\n### \n#  #\n#  #\n### \n": "B",
        " ## \n#  #\n#   \n#   \n#  #\n ## \n": "C",
        "### \n#  #\n#  #\n#  #\n#  #\n### \n": "D",
        "####\n#   \n### \n#   \n#   \n####\n": "E",
        "####\n#   \n### \n#   \n#   \n#   \n": "F",
        " ## \n#  #\n#   \n# ##\n#  #\n ###\n": "G",
        "#  #\n#  #\n####\n#  #\n#  #\n#  #\n": "H",
        " ###\n  # \n  # \n  # \n  # \n ###\n": "I",
        "  ##\n   #\n   #\n   #\n#  #\n ## \n": "J",
        "#  #\n# # \n##  \n# # \n# # \n#  #\n": "K",
        "#   \n#   \n#   \n#   \n#   \n####\n": "L",
        

        " ## \n#  #\n#  #\n#  #\n#  #\n ## \n": "O",
        "### \n#  #\n#  #\n### \n#   \n#   \n": "P",
        "### \n#  #\n#  #\n### \n# # \n#  #\n": "R",
        " ###\n#   \n#   \n ## \n   #\n### \n": "S",
        " ###\n  # \n  # \n  # \n  # \n  # \n": "T",
        "#  #\n#  #\n#  #\n#  #\n#  #\n ## \n": "U",



        "#   \n#   \n # #\n  # \n  # \n  # \n": "Y",
        "####\n   #\n  # \n #  \n#   \n####\n": "Z",
    }
    ret = ""
    arr = re.sub(r"\x1b\[\d*;?\d+m\n?", "", s).replace(fg, "#").replace(bg, " ").split("\n")
    rows, cols = len(arr), len(arr[0])
    chars = math.ceil(cols / 5)
    for i in range(chars):
        st = ""
        for j in range(6):
            st += arr[j][i*5:i*5+4] + "\n"
        if st in letters.keys():
            ret += letters[st]
    return ret

def format_time(time_ns: int):
    """
    Format a time into human-readable units.
    """
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

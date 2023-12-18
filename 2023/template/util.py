import numpy as np
import math
import re

alphabet = "abcdefghijklmnopqrstuvwxyz"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def letter_grid_file(file, separator = ""):
    lines = file.read().splitlines()
    return letter_grid(lines, separator)

def number_grid_file(file, separator = ""):
    lines = file.read().splitlines()
    return number_grid(lines, separator)

def alphabet_scale_grid_file(file, caps=False, separator=""):
    global alphabet
    lines = file.read().splitlines()
    return alphabet_scale_grid(lines, caps, separator)

def letter_grid(lines, separator = ""):
    return [list(l) if separator == "" else l.split(separator) for l in lines]

def number_grid(lines, separator = ""):
    return [list(map(int, list(l))) if separator == "" else list(map(int, l.split(separator))) for l in lines]

def alphabet_scale_grid(lines, caps=False, separator = ""):
    return map(lambda l:
               map(lambda c: ALPHABET.index(c) if caps else alphabet.index(c), l), letter_grid(lines, separator))

def parse_str_6(s, fg = "#", bg = " "):
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

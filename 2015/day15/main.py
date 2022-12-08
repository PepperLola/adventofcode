import sys
import time
import re

class Ingredient:
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories

    def get_values(self, amount):
        return [k * amount for k in [self.capacity, self.durability, self.flavor, self.texture]]

def make_cookie(ingrs, tsp, only_500_calories = False):
    m = {"capacity": 0, "durability": 0, "flavor": 0, "texture": 0, "calories": 0}
    for ingr in ingrs:
        tsps = tsp[ingr.name]
        m["capacity"] += ingr.capacity * tsps
        m["durability"] += ingr.durability * tsps
        m["flavor"] += ingr.flavor * tsps
        m["texture"] += ingr.texture * tsps
        m["calories"] += ingr.calories * tsps

    if len([k for k in m.values() if k <= 0]) > 1 or (only_500_calories and m["calories"] != 500):
        return 0
    return m["capacity"] * m["durability"] * m["flavor"] * m["texture"]

# shared variables here
ingredients = {}

# part 1, takes in lines of file
def p1(lines):
    for line in lines:
        match = re.match(r"(\w+): capacity ([-\d]+), durability ([-\d]+), flavor ([-\d]+), texture ([-\d]+), calories ([-\d]+)", line)
        if match:
            ingredients[match.group(1)] = Ingredient(match.group(1), int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)), int(match.group(6)))

    scores = []
    for sprinkles in range(100):
        for butterscotch in range(100 - sprinkles):
            for chocolate in range(100 - sprinkles - butterscotch):
                candy = 100 - sprinkles - butterscotch - chocolate

                cookie = make_cookie(ingredients.values(), {
                    "Sprinkles": sprinkles,
                    "Butterscotch": butterscotch,
                    "Chocolate": chocolate,
                    "Candy": candy
                })

                scores.append(cookie)
    return max(scores)

# part 2, takes in lines of file
def p2(lines):
    scores = []
    for sprinkles in range(100):
        for butterscotch in range(100 - sprinkles):
            for chocolate in range(100 - sprinkles - butterscotch):
                candy = 100 - sprinkles - butterscotch - chocolate

                cookie = make_cookie(ingredients.values(), {
                    "Sprinkles": sprinkles,
                    "Butterscotch": butterscotch,
                    "Chocolate": chocolate,
                    "Candy": candy
                }, True)

                scores.append(cookie)
    return max(scores)

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

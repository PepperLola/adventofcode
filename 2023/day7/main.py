import sys
import time
import re
import itertools
from functools import total_ordering
from collections import defaultdict, deque
import math
import copy
import numpy as np
from util import format_time, number_grid

# shared variables here
cards_types = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
cards_types.reverse()

@total_ordering
class Hand:
    def __init__(self, cards, bid, part_2=False):
        self.cards = cards
        self.bid = bid
        self.part_2 = part_2

    def get_type(self):
        if not self.part_2 or not "J" in self.cards:
            return Hand.hand_type(self)

        card_freq = {i:self.cards.count(i) for i in cards_types}
        most_common = list(filter(lambda x: x[0] != "J", sorted(card_freq.items(), key=lambda x: x[1])))[-1]
        hand = Hand(self.cards.replace("J", most_common[0]), self.bid)
        return Hand.hand_type(hand)

    @staticmethod
    def hand_type(hand):
        counted = list({i: list(hand.cards).count(i) for i in list(hand.cards)}.values())
        if 5 in counted:
            return 6
        if 4 in counted:
            return 5
        if 3 in counted and 2 in counted:
            return 4
        if 3 in counted:
            return 3
        if counted.count(2) == 2:
            return 2
        if 2 in counted:
            return 1
        return 0

    def __lt__(self, other):
        self_type = self.get_type()
        other_type = other.get_type()
        if self_type == other_type:
            for sc,oc in zip(list(self.cards), list(other.cards)):
                sci, oci = cards_types.index(sc), cards_types.index(oc)
                sci = -1 if sc == "J" and self.part_2 else sci
                oci = -1 if oc == "J" and self.part_2 else oci
                if sci == oci:
                    continue
                return sci < oci
        return self_type < other_type

    def __str__(self):
        return f"Hand[cards={self.cards}, bid={self.bid}]"

#part 1, takes in lines of file
def p1(file, content, lines):
    cds = []
    bids = []
    for line in lines:
        split = line.split(" ")
        cds.append(split[0])
        bids.append(int(split[1]))
    hands = []
    for i in range(len(cds)):
        hands.append(Hand(cds[i], bids[i]))
    hands.sort()
    total = 0
    for i, hand in enumerate(hands):
        total += hand.bid * (i+1)
    return total

# part 2, takes in lines of file
def p2(file, content, lines):
    cds = []
    bids = []
    for line in lines:
        split = line.split(" ")
        cds.append(split[0])
        bids.append(int(split[1]))
    hands = []
    for i in range(len(cds)):
        hands.append(Hand(cds[i], bids[i], True))
    hands.sort()
    total = 0
    for i, hand in enumerate(hands):
        total += hand.bid * (i+1)
    return total

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

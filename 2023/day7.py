from __future__ import annotations
from typing import List

import lib

# Define poker type constants
FIVE_OF_A_KIND = 6
FOUR_OF_A_KIND = 5
FULL_HOUSE = 4
THREE_OF_A_KIND = 3
TWO_PAIR = 2
ONE_PAIR = 1
HIGH_CARD = 0

CARD_ORDERING = {c:i for i, c in enumerate('23456789TJQKA')}

# Tooling will look for triple quotes after definition for documentation.
# See also: https://google.github.io/styleguide/pyguide.html#381-docstrings
class Hand:
    """Represents one hand with 5 cards."""

    def __init__(self, str_hand):
        self.cards, bid = str_hand.split()
        self.bid = int(bid)
        self.type = self.set_type()

    def set_type(self):
        cards = self.cards
        c_count = {}
        for c in cards:
            c_count[c] = c_count.get(c, 0) + 1

        sorted_c = sorted(list(c_count.values()))
        match sorted_c:
            # Five of a kind, where all five cards have the same label: AAAAA
            case [5]:
                return FIVE_OF_A_KIND
            # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
            case [4, 1]:
                return FOUR_OF_A_KIND
            # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
            case [2, 3]:
                return FULL_HOUSE
            # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
            case [1, 1, 3]:
                return THREE_OF_A_KIND
            # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
            case [1, 2, 2]:
                return TWO_PAIR
            # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
            case [1, 1, 1, 2]:
                return ONE_PAIR
            # High card, where all cards' labels are distinct: 23456
            case [1, 1, 1, 1, 1]:
                return HIGH_CARD
            # Not a match with the defined hands, explode
            case _:
                raise ValueError(f"wtf is this??? {sorted_c}")

    # Instead of returning a random object description in debugger, return the string
    def __repr__(self):
        # f"...." is string interpolation, anything in {} gets inlined in the string.
        return f"Hand({self.cards}, {self.bid})"

    # Implement this less than method so one hand can be compared against another
    def __lt__(self, other: Hand):
        zipped_cards = zip(self.cards, other.cards)
        for s, o in zipped_cards:
            if CARD_ORDERING[s] != CARD_ORDERING[o]:
                return CARD_ORDERING[s] < CARD_ORDERING[o]
        # If the two hands are identical for some reason, just return true
        return True

# : List[Hand] || means that the input is a list of Hands
# -> || means that the return value is an int
def total_winnings(str_hands: List[str]) -> int:
    hand_types = {}
    for str_hand in str_hands:
        h = Hand(str_hand)
        hand_types.setdefault(h.type, []).append(h)

    # print(f"before: {hand_types}")
    # Once the inital sorting is done, resort sections based on comparing the first card
    for hand_type in hand_types.values():
        # Compare the first values of the cards, then next, etc.
        hand_type.sort()
    # print(f"after: {hand_types}")
    # Finally, get the final rank and multiply it by its bid
    sorted_list = []
    for t in hand_types.values():
        sorted_list.extend(t)

    total_winnings = 0
    for i, hand in enumerate(sorted_list):
        total_winnings += hand.bid * (i + 1)
    return total_winnings





### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = True
part1 = True

if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    # Multiply instead of sum, works for both parts 1 and 2
    print(total_winnings(input_text.splitlines()))

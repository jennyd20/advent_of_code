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


# Tooling will look for triple quotes after definition for documentation.
# See also: https://google.github.io/styleguide/pyguide.html#381-docstrings
class Hand:
    """Represents one hand with 5 cards."""

    # Constructor
    def __init__(self, str_hand):
        self.cards, bid = str_hand.split()
        self.bid = int(bid)
        self.type = self.set_type()

    # Determine the type of hand at hand construction
    def set_type(self):
        cards = self.cards
        # Count each card in a hand to determine what kind of hand it is
        c_count = {}

        for c in cards:
            c_count[c] = c_count.get(c, 0) + 1

        # Do additional stuff here to turn Jacks into the wildcards
        if not part1:
            j_count = c_count.get("J")
            if j_count:
                # Remove the Jack group and add that nunber to the largest card group
                del c_count["J"]
                # Special case if everything was a Jack
                if not c_count:
                    c_count["A"] = 0
                largest_c = max(c_count.items(), key=lambda x: x[1])
                c_count[largest_c[0]] += j_count

        # Sort the card counts so that they are easy to map to a standard poker hand
        sorted_c = sorted(list(c_count.values()))
        match sorted_c:
            # Five of a kind, where all five cards have the same label: AAAAA
            case [5]:
                return FIVE_OF_A_KIND
            # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
            case [1, 4]:
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

    # Instead of returning a random object description in debugger, return the string describing the hand
    def __repr__(self):
        # f"...." is string interpolation, anything in {} gets inlined in the string.
        return f"Hand({self.cards}, {self.bid})"

    # Implement this less than method so one hand can be compared against another using the basic sort() call
    def __lt__(self, other: Hand):
        zipped_cards = zip(self.cards, other.cards)
        for s, o in zipped_cards:
            if CARD_ORDERING[s] != CARD_ORDERING[o]:
                return CARD_ORDERING[s] < CARD_ORDERING[o]
        # If the two hands are identical for some reason, just return true
        return True


# Defining the expected inputs:
# : List[Hand] || means that the input is a list of Hands
# -> || means that the return value is an int
def total_winnings(str_hands: List[str]) -> int:
    hand_types = {}
    for str_hand in str_hands:
        h = Hand(str_hand)
        hand_types.setdefault(h.type, []).append(h)

    # Make sure to sort the hand types, despite the order they were added
    hand_types = dict(sorted(hand_types.items()))

    # print(f"before: {hand_types}")
    # Once the inital sorting by poker hand is done, resort each based on comparing the first card
    for hand_type in hand_types.values():
        # Compare the first values of the cards, then next, etc.
        hand_type.sort()
    # print(f"after: {hand_types}")

    # Finally, get the final rank and multiply it by its bid
    sorted_list = []
    for t in hand_types.values():
        sorted_list.extend(t)

    # Total winnings are the bid multiplied by the rank
    total_winnings = 0
    for i, hand in enumerate(sorted_list):
        total_winnings += hand.bid * (i + 1)
    return total_winnings


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part1 = False

CARD_ORDERING = None
if part1:
    CARD_ORDERING = {c: i for i, c in enumerate("23456789TJQKA")}
else:
    CARD_ORDERING = {c: i for i, c in enumerate("J23456789TQKA")}

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    print(total_winnings(input_text.splitlines()))

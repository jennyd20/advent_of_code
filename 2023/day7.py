import lib


def total_winnings(hands):
    sorted_hands = []
    for hand in hands:
        type = get_type(hand)
        # Put the hand in with others of its type

    # Once the inital sorting is done, resort sections based on comparing the first card


    # Finally, get the final rank and multiply it by its bid


    return 0

def get_type(hand):
    # 6: Five of a kind, where all five cards have the same label: AAAAA
    # 5: Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    # 4: Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    # 3: Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    # 2: Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    # 1: One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    # 0: High card, where all cards' labels are distinct: 23456

    return 0


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = True
part1 = True

if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    # Multiply instead of sum, works for both parts 1 and 2
    print(total_winnings(input_text.splitlines()))

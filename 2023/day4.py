import lib

extra_card_dict = {}


# Part 1 - calculate the score of each card
def process_card(card):
    scratch_card, card_values = card.split(":")
    values = card_values.split("|")
    winning_nums = reformat_card_nums(values[0])
    my_nums = reformat_card_nums(values[1])

    my_wins = set(winning_nums).intersection(my_nums)
    num_matches = len(my_wins)

    # Part 1
    if part1:
        points = 2 ** (num_matches - 1) if num_matches else 0
        return points

    # Part 2
    scratch_card = scratch_card.split(" ")
    scratch_card_num = int(scratch_card[-1])
    # See how many extra cards are in the table, add additional cards according to the extra
    repeats = extra_card_dict.get(scratch_card_num, 1)
    for i in range(num_matches):
        update_idx = scratch_card_num + 1 + i
        extra_card_dict[update_idx] = extra_card_dict.get(update_idx, 1) + repeats

    return repeats


def reformat_card_nums(card_half):
    return list(filter(None, card_half.split(" ")))


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part1 = False

if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    answer = sum(process_card(card) for card in input_text.splitlines())
    print(str(answer))

import lib

use_example = False

"""
INPUT_TO_INT = {
    "A" : 1,
    "X" : 1,
    "B" : 2,
    "Y" : 2,
    "C" : 3,
    "Z" : 3,
}

INPUT_TO_INT[thr]
"""


# Convert letter inputs to something I can math with
def input_to_int(thr):
    match thr:
        # Rock OR Lose
        case "A" | "X":
            num = 1
        # Paper | Draw
        case "B" | "Y":
            num = 2
        # Scissors | Tie
        case "C" | "Z":
            num = 3
    return num


# For a given Roc-Paper-Scissors matchup, calculate the final score
def score_throw(op_throw, my_throw):
    score = my_throw

    match (my_throw - op_throw) % 3:
        # Tie
        case 0:
            score += 3
        # Win
        case 1:
            score += 6
        # Lose
        case 2:
            pass

    return score


# Day 1 - input is just Col 1 vs Col 2
def score_match_from_throw(match):
    match_list = match.split()
    # Opponent throw: A for Rock, B for Paper, and C for Scissors
    # My throw: X for Rock, Y for Paper, and Z for Scissors
    # Round score: add together
    #   - the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors)
    #   - outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).
    op_throw = input_to_int(match_list[0])
    my_throw = input_to_int(match_list[1])

    return score_throw(op_throw, my_throw)


# Day 2 - figure out what my throw needs to be to get the desired result
def score_match_from_result(match):
    match_list = match.split()
    # Opponent throw: A for Rock, B for Paper, and C for Scissors
    # My desired result: X for lose, Y for draw, and Z for win
    # Round score: add together
    #   - the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors)
    #   - outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

    # Need to choose the throw to match my desired result
    op_throw = input_to_int(match_list[0])
    my_result = input_to_int(match_list[1])
    my_throw = 0

    match my_result:
        # Lose
        case 1:
            my_throw = ((op_throw + 1) % 3) + 1
        # Draw
        case 2:
            my_throw = op_throw
        # Win
        case 3:
            my_throw = ((op_throw) % 3) + 1

    return score_throw(op_throw, my_throw)

if __name__ == "__main__":
  input_text = lib.read_input(__file__, use_example)
  guide = input_text.splitlines()

  # Part 1
  # answer = sum(score_match_throw(match) for match in guide)

  # Part 2
  answer = sum(score_match_from_result(match) for match in guide)

  print(("*** USING EXAMPLE ***: " if use_example else "") + str(answer))

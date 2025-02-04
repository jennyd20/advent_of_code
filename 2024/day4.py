from aoc_libs import grid as grid_lib


def process_input(input, part1):
    grid = grid_lib.Grid.create_from_input(input)

    word_count = 0

    for pos in grid.all_pos_iter():
        # For every character in the grid, check to see if there's the word search XMAS in all 8 directions
        if part1:
            # Only start searching the grid if the first letter is correct
            if grid.get_val(pos) == SEARCH_WORD[0]:
                # print(f"\nFirst letter matches at {pos=}")
                for dir in grid_lib.DIR:
                    if check_for_word(grid, pos, dir):
                        word_count += 1

        # Part2, MAS in the shape of an X
        else:
            # The middle letter that we'll search from is always an A
            if grid.get_val(pos) == "A":
                if check_for_x(grid, pos):
                    word_count += 1
    return word_count


def check_for_word(grid, start_pos, dir):
    # Verified the first letter already, so start traveling along dir to start
    pos = start_pos
    for c in SEARCH_WORD[1:]:
        # print(f"Checking for {c}")
        pos = pos.go_dir(dir)
        if pos.out_of_bounds(grid):
            # print(f"Out of bounds at {pos=}")
            return False
        char = grid.get_val(pos)
        # print(f"Found {char=} at {pos=}")
        if char != c:
            # print(f"No match in {dir=}: {c=} != {char=} at {pos=}")
            return False
    # print(f"Success!! {dir=}")
    return True


def check_for_x(grid, start_pos):
    # print(f"\nChecking at center {row=}, {col=}")
    # Each pair of directions has to be either M or S, but not two of one: (nw, se) and (ne, sw)

    for diag_pair in grid_lib.DIR_DIAG_PAIRS:
        used_m = False
        used_s = False
        for diag_dir in diag_pair:
            pos = start_pos.go_dir(diag_dir)
            if pos.out_of_bounds(grid):
                return False
            # print(f"Checking corner in dir {p}")
            char = grid.get_val(pos)
            # print(f"{char=}")
            used_m = used_m or char == "M"
            used_s = used_s or char == "S"
        if not (used_m and used_s):
            # print("No go")
            return False

    # print("X found")
    return True


########### SCRIPT ARGUMENTS AND EXECUTION ###########
from aoc_libs import lib

SEARCH_WORD = "XMAS"


def main(part1=True, use_example=False):
    input_text = lib.read_input(__file__, use_example)
    return process_input(input_text, part1)


if __name__ == "__main__":
    print(main(part1=True, use_example=False))

from re import L


DIR = {
    "n": (-1, 0),
    "s": (1, 0),
    "w": (0, -1),
    "e": (0, 1),
    "ne": (-1, 1),
    "se": (1, 1),
    "nw": (-1, -1),
    "sw": (1, -1),
}


class Grid:
    def __init__(self, input):
        self.rows = input.splitlines()
        self.max_rows = len(self.rows)
        self.max_cols = len(self.rows[0])

    def get_val(self, row, col):
        return self.rows[row][col]


def process_input(input):
    # For every character in the grid, check to see if there's the word search XMAS in all 8 directions
    grid = Grid(input)

    word_count = 0

    for row in range(grid.max_rows):
        for col in range(grid.max_cols):
            if part1:
                # Only start searching the grid if the first letter is correct
                if grid.get_val(row, col) == SEARCH_WORD[0]:
                    #print(f"\nFirst letter matches at {row=}, {col=}")
                    for dir in DIR:
                        if check_for_word(grid, row, col, dir):
                            word_count += 1

            # Part2, MAS in the shape of an X
            else:
                # The middle letter that we'll search from is always an A
                if grid.get_val(row, col) == "A":
                    if check_for_x(grid, row, col):
                        word_count += 1
    return word_count


def check_for_word(grid, i, j, dir):

    # Verified the first letter already, so start traveling along dir to start
    i, j = update_row_col(i, j, dir)
    for c in SEARCH_WORD[1:]:
        if not coords_in_bounds(grid, i, j):
            #print(f"Out of bounds at {i=}, {j=}")
            return False
        char = grid.get_val(i, j)
        if char != c:
            #print(f"No match in {dir=}: {c=} != {char=} at {i=}, {j=}")
            return False
        else:
            i, j = update_row_col(i, j, dir)
    #print(f"Success!! {dir=}")
    return True


def check_for_x(grid, row, col):
    #print(f"\nChecking at center {row=}, {col=}")
    # Each pair of directions has to be either M or S, but not two of one: (nw, se) and (ne, sw)
    diag_lines = (("nw", "se"), ("ne", "sw"))

    for diag_pair in diag_lines:
        i = None
        j = None
        used_m = False
        used_s = False
        for p in diag_pair:
            i, j = update_row_col(row, col, p)
            if not coords_in_bounds(grid, i, j):
                return False
            #print(f"Checking corner in dir {p}")
            char = grid.get_val(i, j)
            print(f"{char=}")
            used_m = used_m or char == "M"
            used_s = used_s or char == "S"
        if not (used_m and used_s):
            #print("No go")
            return False

    #print("X found")
    return True


def update_row_col(row, col, dir):
    return row + DIR[dir][0], col + DIR[dir][1]


def coords_in_bounds(grid, row, col):
    return 0 <= row < grid.max_rows and 0 <= col < grid.max_cols


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
import lib

SEARCH_WORD = "XMAS"
part1 = False

# Execute the script
if __name__ == "__main__":
    use_example = False
    input_text = lib.read_input(__file__, use_example)

    answer = process_input(input_text)
    print(answer)

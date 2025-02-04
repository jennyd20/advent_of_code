from aoc_libs import grid as grid_lib


def process_input(input, part1):
    map = grid_lib.Grid.create_from_input(input)

    # Figure out where all the
    ant_positions = map.to_dict()

    # Don't care about the blank spaces, just the antenna spaces
    del ant_positions["."]

    all_antinode_pos = set()
    for ant in ant_positions:
        all_antinode_pos.update(calculate_antepodes(map, ant_positions[ant], part1))

    # Prettify the result for debugging purposes
    map.set_all_val_pos("*", all_antinode_pos)
    map.print()

    return len(all_antinode_pos)


def calculate_antepodes(
    map: grid_lib.Grid, pos: set[grid_lib.Position], part1: bool
) -> set[grid_lib.Position]:
    antepodes = set()
    for p1 in pos:
        for p2 in pos:
            if p1 == p2:
                continue
            row_diff = p2.row - p1.row
            col_diff = p2.col - p1.col

            # Find the antepode(s) on both sides of the pair
            antepodes.update(
                get_antepodes_from_point(map, p1, -row_diff, -col_diff, part1)
            )
            antepodes.update(
                get_antepodes_from_point(map, p2, row_diff, col_diff, part1)
            )

    return antepodes


def get_antepodes_from_point(map, start_pos, row_diff, col_diff, part1):
    antepodes = set()
    antepode = grid_lib.Position(start_pos.row - row_diff, start_pos.col - col_diff)
    while antepode.in_bounds(map):
        antepodes.add(antepode)
        antepode = grid_lib.Position(antepode.row - row_diff, antepode.col - col_diff)
        if part1:
            break
    return antepodes


########### SCRIPT ARGUMENTS AND EXECUTION ###########
from aoc_libs import lib


def main(part1=True, use_example=False):
    input_text = lib.read_input(__file__, use_example)
    return process_input(input_text, part1)


if __name__ == "__main__":
    print(main(part1=True, use_example=False))

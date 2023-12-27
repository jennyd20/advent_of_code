import lib


# Types - not the start tile is considered a pipe
GROUND = 7
PIPE = 8

# Directions (also, indices into directional lists)
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3


class Tile:
    """Represents a tile - includes type and directions of exits."""

    def __init__(self, symbol, row, col):
        self.symbol = symbol
        self.row = row
        self.col = col

        self.type = None
        self.exits = [False, False, False, False]
        self.on_loop = False
        self.entry_dir = None

        if symbol == ".":
            self.type = GROUND
        else:
            self.type = PIPE

            # | is a vertical pipe connecting north and south.
            # - is a horizontal pipe connecting east and west.
            # L is a 90-degree bend connecting north and east.
            # J is a 90-degree bend connecting north and west.
            # 7 is a 90-degree bend connecting south and west.
            # F is a 90-degree bend connecting south and east.
            # . is ground; there is no pipe in this tile.
            # S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

            match symbol:
                case "|":
                    self.exits[NORTH] = True
                    self.exits[SOUTH] = True
                case "-":
                    self.exits[EAST] = True
                    self.exits[WEST] = True
                case "L":
                    self.exits[NORTH] = True
                    self.exits[EAST] = True
                case "J":
                    self.exits[NORTH] = True
                    self.exits[WEST] = True
                case "7":
                    self.exits[SOUTH] = True
                    self.exits[WEST] = True
                case "F":
                    self.exits[SOUTH] = True
                    self.exits[EAST] = True
                case "S":
                    # We will eventually know what the exits to the start symbol are
                    pass
                case _:
                    raise ValueError("Invalid pipe symbol")

    def __repr__(self):
        return f"Pipe: {self.symbol} [{self.row}, {self.col}]"


def get_map_and_start(input_text):
    map = []
    start_tile = None
    for x, line in enumerate(input_text.splitlines()):
        tile_line = []
        for y, symbol in enumerate(line):
            added_tile = Tile(symbol, x, y)
            # For the start, we want to know where it is and mark it as part of the loop
            if symbol == "S":
                added_tile.on_loop = True
                start_tile = added_tile
            tile_line.append(added_tile)
        map.append(tile_line)
    return map, start_tile


def print_map(map):
    for line in map:
        row = ""
        for tile in line:
            row += tile.symbol
        print(row)
    print()


def find_loop(map, start_tile):
    loop_tiles = set()
    loop_tiles.add(start_tile)

    loop_tile = None
    entry_dir = None

    # From the start tile, find all adjacent tiles and check to see if they go into the start.
    # Index corresponds to direction - [north, south, east, west]
    possible_exits = []
    for dir in range(4):
        if orthogonal_tile := get_tile_in_dir(map, start_tile, dir):
            opposite_dir = get_opposite_dir(dir)

            if orthogonal_tile.exits[opposite_dir]:
                orthogonal_tile.entry_dir = dir
                possible_exits.append(orthogonal_tile)

    # Critical failure - can't make a loop from the start tile
    assert (
        not len(possible_exits) < 2
    ), f"Not enough exits from start tile: {possible_exits}"

    # TODO - other non-attached pipes can be pointed at the start tile, account for this case.
    assert (
        not len(possible_exits) > 2
    ), f"Many exits from the start tile: {possible_exits}.  Implement this case."

    first_in_loop, last_in_loop = possible_exits

    # Update the start tile to look like a regular pipe tile
    start_tile.exits[first_in_loop.entry_dir] = True
    start_tile.exits[last_in_loop.entry_dir] = True

    # TODO: Programmatically find start tile shape, but just hard code it for now
    start_tile.symbol = "F"

    # Mark the entry direction as false, so there is only one exit from this tile to the next in the loop
    first_in_loop.exits[get_opposite_dir(first_in_loop.entry_dir)] = False
    loop_tile = first_in_loop
    entry_dir = first_in_loop.entry_dir

    # Loop until we're back to the start tile (which starts in the loop_tiles list)
    while not loop_tile in loop_tiles:
        # Add this tile to the list
        loop_tile.on_loop = True
        loop_tiles.add(loop_tile)

        # Mark the direction we came from as no longer an exit
        opposite_dir = get_opposite_dir(entry_dir)
        loop_tile.exits[opposite_dir] = False
        # Get the direction that's the (only) valid exit
        entry_dir = loop_tile.exits.index(True)
        # Get the next tile in the valid direction and continue with that one
        loop_tile = get_tile_in_dir(map, loop_tile, entry_dir)
        assert loop_tile, f"No next tile from direction {entry_dir}"

    return loop_tiles


def find_answer(map, start_tile):
    # Part 1 - Farthest count from the start
    loop_tiles = find_loop(map, start_tile)
    if part1:
        return len(loop_tiles) // 2

    # Part 2 - Find the area enclosed by the loop
    total_inside_tiles = 0
    for row in map:
        inside_tile_count = 0
        inside = False
        horiz_section_start_dir = None
        for col_tile in row:
            # If we are on the loop, we won't be adding anything to the total
            if col_tile.on_loop:
                # Check if we are entering, on, or leaving the loop
                if col_tile.symbol == "|":
                    # Just crossing a boundary, swap inside/outside
                    inside = not inside
                elif col_tile.symbol in ("F", "L"):
                    # Entering a horizontal section, keep track of which direction we're coming in from.
                    # Swap inside/outside at the beginning of the horizontal section
                    horiz_section_start_dir = col_tile.symbol
                    inside = not inside
                elif col_tile.symbol == "-":
                    # Do nothing if we are continuing along the horizontal path
                    pass
                else:
                    # Still on the loop
                    # We are leaving the horizontal section
                    if col_tile.symbol == "|":
                        # Simple boundary crossing, swap inside/outside
                        inside = not inside
                    elif (
                        # If we started from south and end in up, we're in the opposite section of the map
                        horiz_section_start_dir in ("F", "|")
                        and col_tile.symbol == "J"
                    ) or (
                        horiz_section_start_dir in ("L", "|") and col_tile.symbol == "7"
                    ):
                        # Note that we already switched inside/outside at the beginning of the horizontal section, don't need to do it again
                        pass
                    else:
                        # Swap inside/outside back, since we swapped at the beginning of the horizontal section and need to go back to what it was before entering
                        inside = not inside
            # This is not a loop tile
            else:
                # If this tile is inside the loop, add to the count.  Otherwise, don't count it.
                if inside:
                    inside_tile_count += 1

        # Completed a row of the map
        total_inside_tiles += inside_tile_count

    # All rows have been processed
    return total_inside_tiles


def get_tile_in_dir(map, start_tile, dir):
    start_row = start_tile.row
    start_col = start_tile.col

    if dir == NORTH:
        return map[start_row - 1][start_col] if start_row > 0 else None
    if dir == SOUTH:
        return map[start_row + 1][start_col] if start_row < len(map) else None
    if dir == EAST:
        return map[start_row][start_col + 1] if start_col < len(map[0]) else None
    if dir == WEST:
        return map[start_row][start_col - 1] if start_col > 0 else None
    else:
        raise ValueError(f"Invalid direction: {dir}")


def get_opposite_dir(dir):
    if dir == NORTH:
        return SOUTH
    if dir == SOUTH:
        return NORTH
    if dir == EAST:
        return WEST
    if dir == WEST:
        return EAST
    return -1


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part1 = False
alt_input = None
# alt_input = "day10_ex8.txt"

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, alt_input)
    map, start_tile = get_map_and_start(input_text)
    answer = find_answer(map, start_tile)
    print(answer)

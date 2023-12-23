import lib


# Types
GROUND = 7
START = 8  # TODO unneeded?
PIPE = 9

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
        self.in_loop = False

        if symbol == ".":
            self.type = GROUND
        elif symbol == "S":
            self.type = START
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
                added_tile.in_loop = True
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

    # Index corresponds to direction - [north, south, east, west]
    for dir in range(4):
        orthogonal_tile = get_tile_in_dir(map, start_tile, dir)
        opposite_dir = get_opposite_dir(dir)

        # TODO - other non-attached pipes can be pointed at the start, account for this case.
        if orthogonal_tile.exits[opposite_dir]:
            orthogonal_tile.in_loop = True
            orthogonal_tile.exits[opposite_dir] = False
            entry_dir = dir
            loop_tile = orthogonal_tile
            break
    assert loop_tile, f"No next tile from {orthogonal_tile}"

    while not loop_tile in loop_tiles:
        loop_tile.in_loop = True
        loop_tiles.add(loop_tile)

        opposite_dir = get_opposite_dir(entry_dir)
        loop_tile.exits[opposite_dir] = False
        entry_dir = loop_tile.exits.index(True)
        loop_tile = get_tile_in_dir(map, loop_tile, entry_dir)
        assert loop_tile, f"No next tile from direction {entry_dir}"

    return loop_tiles


def find_answer(map, start_tile):
    # Part 1 - Farthest count from the start
    loop_tiles = find_loop(map, start_tile)
    if part1:
        return len(loop_tiles) // 2

    # Part 2 - Find the area enclosed by the loop
    return 0


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
use_example = True
part1 = False
alt_input = None
# alt_input = "day10_ex2.txt"

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, alt_input)
    map, start_tile = get_map_and_start(input_text)
    answer = find_answer(map, start_tile)
    print(answer)

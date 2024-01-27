from __future__ import annotations
import lib
import dataclasses


DIR = {"n": (-1, 0), "s": (1, 0), "e": (0, 1), "w": (0, -1)}


def get_opposite_dir(dir):
    match dir:
        case "n":
            return "s"
        case "s":
            return "n"
        case "e":
            return "w"
        case "w":
            return "e"
        case _:
            raise ValueError("NOT A VALID DIRECTION MEOW")


@dataclasses.dataclass(frozen=True)
class Tile_State:
    x: int
    y: int
    entry_dir: str
    str_dist: int

    # Return a set of possible valid tiles that can be reached from this one.
    def get_next_tstates(self, tstate_heat_dict, input_map):
        # print(f"Processing: {self}")
        # print(f"Current value: {tstate_heat_dict[self]}")
        get_exit_tstates = self.get_exits(input_map)

        # Process next_tiles
        next_tstates = []
        for tstate in get_exit_tstates:
            # print(f"Checking: {tstate}")
            new_tstate_heat = tstate_heat_dict[self] + input_map[tstate.x][tstate.y]
            if tstate not in tstate_heat_dict:
                # print(f"Not in dictionary, updating heat to: {new_tstate_heat}")
                tstate_heat_dict[tstate] = new_tstate_heat
                next_tstates.append(tstate)
            else:
                previous_tstate_heat = tstate_heat_dict[tstate]
                # print(f"State in dictionary, new state: {new_tstate_heat}; previous heat: {previous_tstate_heat}")
                if new_tstate_heat < previous_tstate_heat:
                    # print(f"Updating dictionary state")
                    tstate_heat_dict[tstate] = new_tstate_heat
                    next_tstates.append(tstate)

        # print(f"Returning next states: {next_tstates}")
        # print()
        return next_tstates

    def get_exits(self, map):
        exits = DIR.copy()
        del exits[self.entry_dir]

        # Remove opposite direction if not within the sequence range
        if self.str_dist >= STRAIGHT_DISTANCE_MAX:
            del exits[get_opposite_dir(self.entry_dir)]

        possible_next_tiles = set()
        for exit in exits:
            new_t = self.generate_next_tile(exit)
            if new_t.in_bounds(map):
                possible_next_tiles.add(new_t)
        return possible_next_tiles

    def generate_next_tile(self, exit):
        new_x, new_y = DIR[exit]
        new_straight_count = (
            self.str_dist + 1 if exit == get_opposite_dir(self.entry_dir) else 1
        )
        new_t = Tile_State(
            self.x + new_x,
            self.y + new_y,
            get_opposite_dir(exit),
            new_straight_count,
        )
        return new_t

    def in_bounds(self, input_map):
        return 0 <= self.x < len(input_map) and 0 <= self.y < len(input_map[0])

    def is_exit(self, input_map):
        return self.x == len(input_map) - 1 and self.y == len(input_map[0]) - 1


############ END CLASS DEFINITIONS ############
def least_heat_loss(input_list):
    # Convert the list of strings to a list of list of numbers
    input_map = create_map(input_list)

    # Dictionary from the tile state tuple to the best minimum heat for that state
    tstate_heat_dict = {}

    # (x, y, entry direction, current heat from this path to this location)
    initial_tstate = Tile_State(0, 0, "w", 0)
    tstate_heat_dict[initial_tstate] = 0

    tstate_queue = {initial_tstate}

    # Keep a running total of the minum loss to the exit, cull any paths that are greater than that
    min_heat_loss = 2**32

    while tstate_queue:
        tstate = tstate_queue.pop()
        if tstate.is_exit(input_map):
            min_heat_loss = min(min_heat_loss, tstate_heat_dict[tstate])
        if tstate_heat_dict[tstate] > min_heat_loss:
            continue
        new_tstates = tstate.get_next_tstates(tstate_heat_dict, input_map)
        tstate_queue.update(new_tstates)

    return min_heat_loss


def create_map(input_list):
    map = []
    for row in input_list:
        num_row = []
        for char in row:
            num_row.append(int(char))
        map.append(num_row)
    return map


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
use_example = False
part2 = False
file = ""  # day17_ex2.txt"

STRAIGHT_DISTANCE_MIN = 4 if part2 else 1
STRAIGHT_DISTANCE_MAX = 10 if part2 else 3

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, file)
    input_list = input_text.splitlines()

    answer = least_heat_loss(input_list)
    print(answer)

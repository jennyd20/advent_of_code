from __future__ import annotations
import lib
import dataclasses
from collections import deque


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
    def get_new_tile_tuples(
        self, current_path_heat, tile_heat_dict, map
    ) -> list[tuple[Tile_State, int]]:
    
        get_exit_tiles = self.get_exits(map)

        # Process next_tiles
        tiles_to_queue = []
        for new_tile in get_exit_tiles:
            path_heat_to_new_tile = current_path_heat + map[new_tile.x][new_tile.y]
            if new_tile not in tile_heat_dict:
                # print(f"- t not in dictionary")
                tiles_to_queue.append((new_tile, path_heat_to_new_tile))
            else:
                # print(f"- Tile in dictionary: {t}")
                previous_heat = tile_heat_dict[new_tile]
                # print(f"-- Old_heat: {old_heat} vs new path heat: {path_heat}")
                if path_heat_to_new_tile < previous_heat:
                    tile_heat_dict[new_tile] # blagh
                    # Update adjacent tiles
                pass

        print(f"{tiles_to_queue=}")
        print("##########")
        return tiles_to_queue

    def get_exits(self, map):
        exits = DIR.copy()
        del exits[self.entry_dir]

        # Remove opposite direction if not within the sequence range
        if self.str_dist >= STRAIGHT_DISTANCE_MAX - 1:
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
            self.str_dist + 1 if exit == get_opposite_dir(self.entry_dir) else 0
        )
        new_t = Tile_State(
            self.x + new_x,
            self.y + new_y,
            get_opposite_dir(exit),
            new_straight_count,
        )
        return new_t

    def in_bounds(self, map):
        return 0 <= self.x < len(map) and 0 <= self.y < len(map[0])

    def is_exit(self, map):
        return self.x == len(map) - 1 and self.y == len(map[0]) - 1


############ END CLASS DEFINITIONS ############
def least_heat_loss(input_list):
    # Convert the list of strings to a list of list of numbers
    map = create_map(input_list)

    # Create the starting tile and add it to the processing list
    # Dictionary from the tile state tuple to the current minimum heat
    tile_heat_dict = {}

    # (x, y, entry direction, current heat from this path to this location)
    starting_tile = Tile_State(0, 0, "w", 0)

    # Process queue values consists of a set of (tile, current heat)
    tile_process_queue: deque[tuple[Tile_State, int]] = deque([(starting_tile, 0)])

    while tile_process_queue:
        current_tile_tuple = tile_process_queue.popleft()
        new_tile_tuples = process_tile(current_tile_tuple, tile_heat_dict, map)
        if new_tile_tuples:
            [tile_process_queue.append(t) for t in new_tile_tuples]

    # Calculate heat loss
    min_paths_heat = MAX_INT
    for t in tile_heat_dict:
        if t.is_exit(map):
            min_paths_heat = min(min_paths_heat, tile_heat_dict[t])

    return min_paths_heat


def process_tile(tile_tuple, tile_heat_dict, map):
    tile, current_path_heat = tile_tuple

    # TODO - check this logic
    if not tile in tile_heat_dict:
        # print(f"Process tile {tile}")
        # This state is new or is being updated, so add valid next tiles to the list
        tile_heat_dict[tile] = current_path_heat
        # print(f"Tile From dict: {current_heat=}")
        return tile.get_new_tile_tuples(current_path_heat, tile_heat_dict, map)
    
    if current_path_heat < tile_heat_dict[tile]:
        # Somehow remove the already-added tiles from the queue
        pass

    # Otherwise nothing changed, so add no new tiles to process
    return None


def create_map(input_text):
    map = []
    for row in input_list:
        num_row = []
        for char in row:
            num_row.append(int(char))
        map.append(num_row)
    return map


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = True
part2 = False
file = None  # "day17_ex2.txt"


MAX_INT = 2**32
STRAIGHT_DISTANCE_MIN = 0
STRAIGHT_DISTANCE_MAX = 3

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, file)
    input_list = input_text.splitlines()

    answer = least_heat_loss(input_list)
    print(answer)

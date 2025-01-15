from aoc_libs import grid as grid_lib


def process_input(input):
    map = grid_lib.Grid(input)

    # Get initial guard position
    guard_pos = map.find_first_val("^")
    guard_pos.dir = "n"

    # Change the guard's starting position element, so we can cross over it in the future
    # Can probably just check for obstacles rather than empty floor instead, but this is
    # easy to do.
    map.set_val(guard_pos, ".")

    guard_paths = walk_guard(map, guard_pos.copy())

    if part1:
        return len(guard_paths)

    else:
        total = 0
        for r, c in guard_paths:
            new_block_pos = grid_lib.Position(r, c)
            # TODO: just set the value and set it back, rather than making a full new copy
            adjusted_map = map.copy().set_val(new_block_pos, "#")
            path = walk_guard(adjusted_map, guard_pos.copy())
            if not path:
                # print(f"Successfully found a loop when placing a block at {new_block_pos}")
                total += 1

        return total


def walk_guard(map, guard_pos):
    # Track the paths that the guard will follow in a set
    guard_paths = {(guard_pos.get_coords(), guard_pos.dir)}
    while True:
        new_pos = guard_pos.copy().forward()

        if new_pos.out_of_bounds(map):
            # The Elvis Guard has left the building, we're done!
            break

        # If this new position has matching coords AND direction in the path,
        # then we're in a loop.  Exit with empty path (a falsy value)
        new_pos_coords = new_pos.get_coords()
        new_pos_dir = new_pos.dir
        set_key = (new_pos_coords, new_pos_dir)

        if set_key in guard_paths:
            # print(f"keys match, we're in a loop")
            return {}

        # if new_pos_coords in guard_paths:
        #     previous_dir = guard_paths[new_pos_coords]
        #     if previous_dir == new_pos.dir:
        #         print(f"{new_pos=}, {previous_dir=}")
        #         return {}

        if map.get_val(new_pos) == "#":
            guard_pos.rotate()
        else:
            guard_paths.add(set_key)
            guard_pos = new_pos

    # Right now, guard_paths is a full set of locations and directions
    # Remove duplicates where the coords match, even if the dirs don't

    return {coords for coords, _ in guard_paths}


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
part1 = False
use_example = False

# Execute the script
from aoc_libs import lib

if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    answer = process_input(input_text)
    print(answer)

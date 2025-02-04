from aoc_libs import grid as grid_lib


def process_input(input, part1):
    map = grid_lib.Grid.create_from_input(input)

    # Get initial guard position
    guard_pos = map.get_first_val("^")
    guard_pos_dir = grid_lib.PositionAndDirection(guard_pos, grid_lib.Dir.N)

    # Change the guard's starting position element, so we can cross over it in the future
    # Can probably just check for obstacles rather than empty floor instead, but this is
    # easy to do.
    map.set_val(guard_pos, ".")

    guard_poses = walk_guard(map, guard_pos_dir)

    if part1:
        return len(guard_poses)

    else:
        # Count the total number of places you can put an obstruction to form a loop
        total = 0
        # print(f"Num of positions to check: {len(guard_poses)}")
        # For every position the guard visits, try to put an obstacle in that spot.
        for pos in guard_poses:
            # Literally change a position to an obstacle (#) on the map, then try to walk the guard
            # print(f"Obstacle at {pos=}")
            map.set_val(pos, "#")
            path = walk_guard(map, guard_pos_dir)
            map.set_val(pos, ".")
            if not path:
                # print(f"Successfully found a loop when placing a block at {pos}")
                total += 1

        return total


# Walk the guard along the map from the given starting position
# The guard walks in a straight line until it hits an obstacle - then it turns right.
def walk_guard(
    map, guard_pos_dir: grid_lib.PositionAndDirection
) -> set[grid_lib.Position]:
    # Track the paths that the guard will follow in a set
    guard_paths: set[grid_lib.PositionAndDirection] = {guard_pos_dir}
    while True:
        new_pos_dir = guard_pos_dir.forward()

        if new_pos_dir.pos.out_of_bounds(map):
            # The Elvis Guard has left the building, we're done!
            break

        # If this new position has matching coords AND direction in the path,
        # then we're in a loop.  Exit with empty path (a falsy value)
        if new_pos_dir in guard_paths:
            # print(f"keys match, we're in a loop")
            return set()

        if map.get_val(new_pos_dir.pos) == "#":
            guard_pos_dir = guard_pos_dir.rotate()
        else:
            guard_paths.add(new_pos_dir)
            guard_pos_dir = new_pos_dir

    # Right now, guard_paths is a full set of locations and directions
    # Remove duplicates where the coords match, even if the dirs don't

    return {x.pos for x in guard_paths}


########### SCRIPT ARGUMENTS AND EXECUTION ###########
from aoc_libs import lib


def main(part1=True, use_example=False):
    input_text = lib.read_input(__file__, use_example)
    return process_input(input_text, part1)


if __name__ == "__main__":
    print(main(part1=False, use_example=False))

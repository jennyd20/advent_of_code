import lib


DIR = {"u": (-1, 0), "d": (1, 0), "l": (0, -1), "r": (0, 1)}


class laser:
    # Constructor
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.vert = True if dir == DIR["u"] or dir == DIR["d"] else False

    # This updates the direction as well as the vertical check
    def set_dir(self, dir):
        self.dir = dir
        self.vert = True if dir == DIR["u"] or dir == DIR["d"] else False

    def __repr__(self):
        return f"Laser(({self.x}, {self.y}) dir: {self.dir})"


def num_energized_tiles(light_contraption):
    # Add the initial laser(s) to the list of lasers (we start outside the grid)
    lasers = []
    if not part2:
        lasers.append(laser(0, -1, DIR["r"]))
    else:
        # Generate a list of all input lasers
        x = len(light_contraption)
        y = len(light_contraption[0])

        # Construct lasers for the left/right edges at the same time
        for i in range(x):
            new_laser_1 = laser(i, -1, DIR["r"])
            new_laser_2 = laser(i, y, DIR["l"])
            lasers += [new_laser_1, new_laser_2]

        # Construct lasers for the up/down edges at the same time
        for j in range(y):
            new_laser_1 = laser(-1, j, DIR["d"])
            new_laser_2 = laser(x, j, DIR["u"])
            lasers += [new_laser_1, new_laser_2]

    laser_energy = set()
    while lasers:
        laser_energy.add(get_laser_energy(lasers.pop(), light_contraption))

    return max(laser_energy)


def get_laser_energy(initial_laser, light_contraption):
    visited_routes = set()
    sub_lasers = [initial_laser]
    while sub_lasers:
        sub_lasers += follow_laser(sub_lasers.pop(), light_contraption, visited_routes)

    total = get_energy_sum(visited_routes)
    return total


# Routes are stored as a tuple in a set, but we want to just get the count of the tiles and not their entry directions
def get_energy_sum(routes):
    energized_tiles = set()
    for i in routes:
        energized_tiles.add(i[0])
    return len(energized_tiles)


# Follow a laser through its path, marking visited routes and splitting into new lasers when required
def follow_laser(input_laser, light_contraption, visited_routes):
    new_lasers = []
    x = input_laser.x
    y = input_laser.y

    while True:
        # Advance in the direction specified by the laser
        new_x, new_y = input_laser.dir
        x += new_x
        y += new_y

        # Stop this laser if it will fall off the contraption
        if not (0 <= x < len(light_contraption) and 0 <= y < len(light_contraption[0])):
            break

        # Stop this laser if we've already processed this tile from this direction
        key = ((x, y), input_laser.dir)
        if key in visited_routes:
            break
        else:
            visited_routes.add(key)

        # Advance the laser based on its position in the contraption
        match light_contraption[x][y]:
            case ".":
                # This is ground, do nothing
                pass
            case "/":
                # Mirror - Bend the laser depending on the angle coming in
                if input_laser.dir == DIR["u"]:
                    input_laser.set_dir(DIR["r"])
                elif input_laser.dir == DIR["d"]:
                    input_laser.set_dir(DIR["l"])
                elif input_laser.dir == DIR["l"]:
                    input_laser.set_dir(DIR["d"])
                elif input_laser.dir == DIR["r"]:
                    input_laser.set_dir(DIR["u"])
                else:
                    raise ValueError
            case "\\":
                # Mirror - Bend the laser depending on the angle coming in
                if input_laser.dir == DIR["u"]:
                    input_laser.set_dir(DIR["l"])
                elif input_laser.dir == DIR["d"]:
                    input_laser.set_dir(DIR["r"])
                elif input_laser.dir == DIR["l"]:
                    input_laser.set_dir(DIR["u"])
                elif input_laser.dir == DIR["r"]:
                    input_laser.set_dir(DIR["d"])
                else:
                    raise ValueError
            # Splitters next: stop the input laser and add the two new split lasers to the list
            case "-":
                if input_laser.vert:
                    new_lasers.append(laser(x, y, DIR["l"]))
                    new_lasers.append(laser(x, y, DIR["r"]))
                    break
                # Else this is horizontal, treat this as an empty space and continue
            case "|":
                if not input_laser.vert:
                    new_lasers.append(laser(x, y, DIR["u"]))
                    new_lasers.append(laser(x, y, DIR["d"]))
                    break
                # Else this is vertical, treat this as an empty space and update nothing
            case _:
                raise ValueError("Invalid contraption")

    return new_lasers


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part2 = True

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    input_list = input_text.splitlines()

    answer = num_energized_tiles(input_list)
    print(answer)

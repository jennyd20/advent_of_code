from aoc_libs.grid import Position as Position
from aoc_libs.grid import Grid as Grid
import dataclasses

@dataclasses.dataclass
class HikingPos:
    pos: Position
    val: int
    next_poses: list[Position]
    valid: bool

def process_input(input):
    map = Grid.create_from_input(input, new_type = int)
    return None



# For each position in the map:
# - Follow valid paths - adjacent positions that are +1 from the existing position value
# - If those positions can reach a 9 (successful path) - record all these "success" positions
#   in a data structure that records the total number of successful paths from that node
# - If not: put those positions into a "failure" structure.  If we hit these positions
#   in the future, we can prune that search path
# For future non-visited positions:
# - If you hit a visited position, either add it to the failure set or add that
#   pos to the success set, setting the 9s value to the 9s val of the met pos
# 

########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
part1 = False
use_example = False

# Execute the script
from aoc_libs import lib

if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    answer = process_input(input_text)
    print(answer)

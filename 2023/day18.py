import lib


def process_input(input_text, part2=False):
    plan = get_plan_from_input(input_text, part2)
    corner_list = get_corner_coords(plan)
    slice_dict = create_slice_dict(corner_list)
    total = find_final_area(slice_dict)
    return total


# Converts raw input strings into a list of individual instructions, where the distance has been converted to an int
def get_plan_from_input(input_text, part2=False):
    plan = []
    # Create a list of processable lines from the whole input text
    # Convert the number characters to digits
    for row in input_text.splitlines():
        dir, dist, color = row.split(" ")
        new_instr = None
        if not part2:
            new_instr = [dir, int(dist)]
        else:
            new_instr = convert_color_to_instruction(color)
        plan.append(new_instr)
    return plan


NUM_TO_DIR = {0: "R", 1: "D", 2: "L", 3: "U"}


def convert_color_to_instruction(color):
    dist_str = color[2:-2]
    dist = int(dist_str, 16)
    dir_int = int(color[-2:-1])
    dir = NUM_TO_DIR[dir_int]
    return [dir, dist]


# Trace the route in the plan
# Record coordinates of corners, where the path turns
# Return a sorted list, starting from the bottom left corner, giong up and then right
def get_corner_coords(plan):
    corners = []
    x = 0
    y = 0
    for instruction in plan:
        # Because we're tracing the path, keep track of coordinates between each instruction
        x, y = find_corner(instruction, corners, x, y)
    corners.sort()
    return corners


# Add add or subtract along the appropriate axis to generate the next corner
def find_corner(instruction, corners, x, y):
    dir, dist = instruction

    offset = dist if (dir == "R" or dir == "U") else -dist
    # Note: input is guaranteed to begin at a corner, not in the middle of a line
    if dir in ("L", "R"):
        x += offset
    else:
        y += offset

    corners.append((x, y))
    return x, y


# Create a dictionary mapping all pairs of corners into a "slice" with key of its x index and value of the y1, y2 values of the pairs
# In the end, the dict will contain as keys only indices of x coords, with the value being a list of all slices at that index
def create_slice_dict(corner_list):
    dict = {}
    # Process corners a pair at a time, since they will always match up in a column
    for i in range(0, len(corner_list) - 1, 2):
        x, y1 = corner_list[i]
        _, y2 = corner_list[i + 1]
        dict.setdefault(x, []).append((y1, y2))
    return dict


# Given the dictionary of x axis locations of y axis slice definitions, find the area of the enclosed space
def find_final_area(slice_dict: dict[int, list[tuple[int, int]]]) -> int:
    area_total = 0
    prior_idx = None
    prior_slices = []

    for x_idx in slice_dict:
        if prior_idx == None:
            prior_idx = x_idx - 1
        x_area, prior_slices = process_index(
            x_idx, slice_dict[x_idx], prior_idx, prior_slices
        )
        area_total += x_area
        prior_idx = x_idx
    return area_total


# For this column at this index, find the area of the prior section between slices
# Then find the new set of slices that will continue forward in the map from this point
# Then can find the area of all the wall and internal area at the current index
def process_index(x_idx, x_slices, prior_idx, prior_slices):
    new_area = 0

    mid_area = calculate_area_between_indices(prior_slices, prior_idx, x_idx)
    new_area += mid_area
    next_slices = generate_next_slices(prior_slices, x_slices)
    merged_slices = merge_slices(prior_slices, next_slices)
    column_area = calculate_column_area(merged_slices)
    new_area += column_area

    return new_area, next_slices


# Finding the area of the slices between the last index and this one.
# Do not include the columns at either index.
def calculate_area_between_indices(slice_list, prior_x_idx, scan_idx):
    area = 0
    for slice in slice_list:
        s1, s2 = slice

        # Add the area - width (non-inclusive) * height (inclusive)
        width = scan_idx - prior_x_idx - 1
        height = s2 - s1 + 1
        area += width * height
    return area


# Simple sum of the total heights of all the slices at this index (in the column)
def calculate_column_area(slices):
    area = 0
    for slice in slices:
        y1, y2 = slice
        area += y2 - y1 + 1
    return area


def generate_next_slices(prior_slices, current_slices):
    new_slices = prior_slices
    for current in current_slices:
        new_slices = next_slices_from_current(new_slices, current)
    return new_slices


def next_slices_from_current(slices, current):
    if not slices:
        return [current]

    c1, c2 = current
    for idx, (p1, p2) in enumerate(slices):

        # If these slices are exactly the same, remove that slice
        if p1 == c1 and p2 == c2:
            return slices[:idx] + slices[idx + 1 :]

        # If the current is below the prior slice, insert it before
        if c2 < p1 - 1:
            return slices[:idx] + [current] + slices[idx:]

        # If there's another slice to check, see if current will fill in between them
        if idx < len(slices) - 1:
            next_p1, next_p2 = slices[(idx + 1)]
            if p2 == c1 and c2 == next_p1:
                return slices[:idx] + [(p1, next_p2)] + slices[(idx + 2) :]

        # Check for current overlapping the top of prior
        if p2 == c1:
            return slices[:idx] + [(p1, c2)] + slices[idx + 1 :]

        # Check for current overlapping the bottom of prior
        if c2 == p1:
            return slices[:idx] + [(c1, p2)] + slices[idx + 1 :]

        # Check for internal overlap with prior
        if c1 == p1:
            return slices[:idx] + [(c2, p2)] + slices[idx + 1 :]
        if c2 == p2:
            return slices[:idx] + [(p1, c1)] + slices[idx + 1 :]

        # Check if we need to split into two new slices
        if c1 > p1 and c2 < p2:
            return slices[:idx] + [(p1, c1), (c2, p2)] + slices[idx + 1 :]

    # If we get through all the slices and haven't inserted the current slice yet, add it to the end
    return slices + [current]


# From a list of slices, merge them all together to the minimum non-overlapping set
def merge_slices(prior_slices, current_slices):
    # Combine the lists and then sort.
    # Then compare each adjacent pair in the list to see if there's any overlap.
    # The sorted list means that the lower bounds of each slice will be more than or equal to the slice before it
    slices = prior_slices + current_slices
    slices.sort()

    i = 0
    while i < len(slices) - 1:
        p1, p2 = slices[i]
        next_p1, next_p2 = slices[i + 1]
        # If there's an overlap between these two slices, combine them.
        # Since these slices are sorted, the lower bound will strictly increase
        if next_p1 <= p2:
            merged = (p1, max(p2, next_p2))
            slices = slices[:i] + [merged] + slices[i + 2 :]
        else:
            i += 1
    return slices


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
use_example = False
alt_input = ""
part2 = True
import textwrap

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, alt_input)

    answer = process_input(input_text, part2)
    print(answer)

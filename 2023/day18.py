import lib


def process_input(input_text):
    plan = create_plan(input_text)
    corner_map = get_corner_coords_map(plan)
    total = find_area(corner_map)
    return total, corner_map


# Converts strings into a list of individual instructions, where the direction has been converted to an int
def create_plan(input_text):
    plan = []
    # Create a list of lines
    # Convert the word numbers to digits
    for row in input_text.splitlines():
        dir, dist, color = row.split(" ")
        plan.append([dir, int(dist), color])
    return plan


# Trace the route in the plan
# Record coordinates of corners, where the path turns
def get_corner_coords_map(plan):
    corners = []
    x = 0
    y = 0
    for instruction in plan:
        # Because we're tracing the path, keep track of where we are between each instruction
        x, y = process_line(instruction, corners, x, y)
    corners.sort()
    return corners


def process_line(instruction, corners, x, y):
    dir, dist, color = instruction

    offset = dist if (dir == "R" or dir == "U") else -dist
    # Note: input is guaranteed to begin at a corner, not in the middle of a line
    if dir in ("L", "R"):
        x += offset
    else:
        y += offset

    corners.append((x, y))
    return x, y

    # # Set up a dictionary where each row (key) contains a list (value) of starting idx and length of any given run in that row
    # # In the vertical case, need to add a single width at each x value in the range
    # if dir in ("U", "D"):
    #     for i in range(dist - 1):
    #         row_offset = i + 1
    #         if dir == "U":
    #             row_offset = -row_offset
    #         corners.setdefault(x + row_offset, []).append((y, 1))
    #     x += dist if dir == "D" else -dist

    # elif dir in ("L", "R"):
    #     y_offset = y + (dist if dir == "R" else -dist)
    #     col_idx_lower = min(y, y_offset)
    #     corners.setdefault(x, []).append((col_idx_lower, dist + 1))
    # #     y = y_offset

    # else:
    #     raise ValueError("Nope")

    # return x, y


# def find_total(border_dict):
#     total = 0
#     for row_key in border_dict.keys():
#         in_loop = False
#         # Process edges from left to right, so sort the values
#         values = sorted(border_dict[row_key])
#         scan_idx = values[0][0]
#         for i in values:
#             start_idx, dist = i
#             if start_idx > scan_idx:
#                 in_loop = not in_loop
#             if in_loop:
#                 total += start_idx - scan_idx
#             total += dist
#             scan_idx = start_idx + dist
#         pass
#     return total



def find_area(corners):
    area_total = 0
    height = 0
    prior_slice_idx = None
    max_y = 0
    min_y = 0
    for i in range(0, len(corners) - 1, 2):
        x, y1 = corners[i]
        _, y2 = corners[i + 1]

        # Set up the initial scan line
        if i == 0:
            prior_slice_idx = x - 1
            height = (y2 - y1 + 1)
        
        # Check the new x index vs the old one
        if x == prior_slice_idx:
            # Another pair of corners in the same x axis - jigging in and out to make a cove
            pass

        # Add prior rectangle
        width = x - prior_slice_idx + 1
        area_total += width * height

        # Set up y height of new rectangle area
        new_height = (y2 - y1 + 1)
        # Subtract the bit that overlaps with the last rectangle, so we don't double count
        area_total -= new_height


        prior_slice_idx = x
        #else:
    return area_total


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
use_example = True
alt_input = ""
#alt_input = "day18_ex2.txt"
# alt_input = "day18_ex3.txt"
# alt_input = "day18_ex4.txt"
# alt_input = "day18_ex5.txt"
part2 = False

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, alt_input)

    answer, dict = process_input(input_text)
    print(answer)


# Note: this has a lot in common with Day 10, with looping and finding the internal area of the loop.

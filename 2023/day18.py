import lib


def process_input(input_text):
    plan = get_plan_from_input(input_text)
    corner_list = get_corner_coords(plan)
    slice_dict = create_slice_dict(corner_list)
    total = find_final_area(slice_dict)
    return total


# Converts raw input strings into a list of individual instructions, where the distance has been converted to an int
def get_plan_from_input(input_text):
    plan = []
    # Create a list of processable lines from the whole input text
    # Convert the number characters to digits
    for row in input_text.splitlines():
        dir, dist, color = row.split(" ")
        plan.append([dir, int(dist), color])
    return plan


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
    dir, dist, color = instruction

    offset = dist if (dir == "R" or dir == "U") else -dist
    # Note: input is guaranteed to begin at a corner, not in the middle of a line
    if dir in ("L", "R"):
        x += offset
    else:
        y += offset

    corners.append((x, y))
    return x, y


# Create a dictionary mapping all pairs of corners into a "slice" with key of its x index and value of the y1, y2 values of the pairs
# In the end, the dict will contain only indices of x coords with slices, and each one will contain all slices at that index
def create_slice_dict(corner_list):
    dict = {}
    # Process corners a pair at a time, since they will always match up in a column
    for i in range(0, len(corner_list) - 1, 2):
        x, y1 = corner_list[i]
        _, y2 = corner_list[i + 1]
        dict.setdefault(x, []).append((y1, y2))
    return dict


# Given the dictionary of x locations and y slice definitions, find the area of the enclosed space
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


# For this column at this x index, find the area of the prior mid section between slices, then find the new set of walls based on the current slices
# Then can find the area of the new set of walls and determine the starting slices for the next portion of the map (not including parts that are not outside)
def process_index(x_idx, x_slices, prior_idx, prior_slices):
    new_area = 0
    new_slices = []

    new_area += calculate_middle_area(prior_slices, prior_idx, x_idx)
    new_slices = calculate_next_slices(prior_slices, x_slices)
    merged_slices = calculate_merged_slices(prior_slices, new_slices)
    new_area += calculate_index_area(merged_slices)

    # merged_slices = merge_slices(prior_slices, x_slices)
    # new_slices = calculate_next_slices(prior_slices, merged_slices)

    #     X#####X
    #     X###X #
    #         # #
    # X#######X #
    # #   X#####X
    # X###X
    # 01234567890

    # 5     X     X
    # 4     X   X
    # 3
    # 2 X       X
    # 1     X     X
    # 0 X   X
    #   01234567890
    #           ^ 1
    #
    # x:4
    # prior_slices = [(0, 2)]   x_slices = [(0, 1), (4, 5)]
    #
    # new_slices = [(1, 2), (4, 5)]
    #
    # x:8
    # prior_slices = [(1, 2), (4, 5)]   x_slices = [(2, 4)]
    #
    # new_slices = [(1, 5)]
    #
    # x:10
    # prior_slices = [(1, 5)]   x_slices = [(1, 5)]
    #
    # new_slices = []

    return new_area, new_slices


# Finding the area of the slices between the last index and this one.  Do not include the slices on either index.
def calculate_middle_area(slice_list, prior_x_idx, scan_idx):
    area = 0
    for slice in slice_list:
        s1, s2 = slice

        # Add the area - width (non-inclusive) * height (inclusive)
        width = scan_idx - prior_x_idx - 1
        height = s2 - s1 + 1
        area += width * height
    return area


# Simple sum of the total heights of all the slices at this index (in the column)
def calculate_index_area(slices):
    area = 0
    for slice in slices:
        y1, y2 = slice
        area += y2 - y1 + 1
    return area


# Find the overlap between the prior slices and the new merged slices to determine the indices of the new slices going forward
# This will only add slices that represent being inside the loop
# def calculate_next_slices(prior_slices, current_slices):
#     # If we're not comparing against prior slices, the current slices will be the next ones
#     if not prior_slices:
#         return current_slices

#     next_slices = []
#     for prior in prior_slices:
#         for current in current_slices:
#             # Get the union of this pair of slices# TODO: WORK HERE!!!oving forward in the grid
#             next_slices += get_slice_union(prior, current)
#     return next_slices


# prior_slices = [(0, 2)]   current_slices = [(0, 1), (4, 5)]
#
# new_slices = [(1, 2), (4, 5)]
def calculate_next_slices(prior_slices, current_slices):
    new_slices = prior_slices
    for slice in current_slices:
        new_slices = calculate_new_slice_list(new_slices, slice)
    return new_slices


#         slices = [(0, 2)]   current = (0, 1)
# result: new_slices = [(1, 2)]
#
#         slices = [(1, 2)]   current = (4, 5)
# result: new_slices = [(1, 2), (4, 5)]
#
#         slices = [(1, 2), (4, 5)]   current = (2, 4)
# result: new_slices = [(1, 5)]
#
#         slices = [(1, 5)]   current = [(1, 5)]
# result: new_slices = []


def calculate_new_slice_list(slices, current):
    if not slices:
        return [current]
    
    c1, c2 = current

    # possible interactions of "current" with stuff in "slices":
    # 1) insert a new slice somewhere, don't modify existing slices
    #       - non overlapping, non-adjacent
    # 2a) replace an existing slice because "current" is adjacent to it
    # 2b) replace two existing slices because "current" is in the middle (adjacent needed?) or overlapping to both
    # 3) modify one existing slice
    #       - overlapping case (one end will be the same)
    # 4) remove a slice where current matches exactly

    #  (c1, c2)
    #
    #      0          1         2
    # [ (p1, p2), (p1, p2), (p1, p2)]

    # Case 2 - adjacent
    #
    # X
    # #
    # X#########X
    #    X######X
    #    #
    #    X

    # Case 2b
    #
    #  X
    #  #
    #  X#X
    #    #
    #  X#X
    #  #
    #  X
    #

    # Case ??
    #
    #  X
    #  #
    #  X#X
    #    X### 2) merge this as a separate slice with the chunk below
    #    X### 1) merge this with the bottom as an overlap
    #  X#X
    #  #
    #  X
    #

    # Case 3 - overlapping
    #
    # X
    # #
    # X  X
    #    #
    #    #
    #    X

    for idx, (p1, p2) in enumerate(slices):

        # case 4) If these slices are exactly the same, then remove that slice
        if p1 == c1 and p2 == c2:
            return slices[:idx] + slices[idx + 1 :]

        # case 1) where we insert before 'idx':
        if c2 < p1 - 1:
            return slices[:idx] + [current] + slices[idx:]

        # SKIP---> case 2a) where new slice is adjacent to (p1, p2)
        # if c2 == (p1 - 1):
        #     return

        # # In the final case, just append this slice to the list
        # if idx == len(slices) - 1:
        #     return slices + [current]

        # If there's another slice to check, see if current will fill in between them
        if idx < len(slices) - 1:
            # case 2b) where 'current' fills the gap between "idx" and "idx+1" slices:
            next_p1, next_p2 = slices[(idx + 1)]
            if p2 == c1 and c2 == next_p1:
                return slices[:idx] + [(p1, next_p2)] + slices[(idx + 2) :]


        # case 3) where 'current' overlaps one of the ends:
        #
        #          (c1, c2)
        #     (p1, p2)       -> (p1, c2)
        #
        # c2 X        X
        #    #
        #    #
        # c1 X X p2
        #      #
        #      X p1   X
        #
        # ---------------------------
        #
        #          (c1,      c2)
        #          (p1, p2)       -> (p2, c2)
        #
        # c2 X        X
        #    #
        #    # X p2   X
        # c1 X X p1
        #
        # ---------------------------

        # Check for current overlapping the top of prior
        if p2 == c1:
            return slices[:idx] + [(p1, c2)] + slices[idx + 1 :]

        # Check for current overlapping the bottom of prior
        if c2 == p1:
            return slices[:idx] + [(c1, p2)] + slices[idx + 1 :]
        
        # Check for internal overlap with prior
        if c1 == p1:
            return slices[:idx] + [(c2, p2)] + slices[idx + 1:]
        if c2 == p2:
            return slices[:idx] + [(p1, c1)] + slices[idx + 1:]
            

    raise ValueError("WTF")
    # return slices


# def get_slice_union(prior, current):
#     # This should never be called with empty slices
#     assert prior and current

#     p1, p2 = prior
#     c1, c2 = current

#     # If these slices are exactly the same, then just return the new slice
#     if p1 == c1 and p2 == c2:
#         return [(c1, c2)]

#     # If these slices are non-overlapping and non-adjacent, return both
#     if p1 > c2 + 1 or p2 < c1 - 1:
#         return [prior, current]

#     # If they are adjacent, merge them
#     if p1 == c2 + 1:
#         return [(c1, p2)]

#     if p2 == c1 - 1:
#         return [(p1, c2)]

#     # Otherwise, they are overlapping
#     prior_h = p2 - p1
#     current_h = c2 - c1
#     diff = prior_h - current_h
#     if p1 < c1:
#         return [(p1, p1 + diff)]
#     if p2 > c2:
#         return [c2, c2 + diff]

#     raise ValueError("Slice union broke!")


# TODO: brain this
# From a list of slices, merge them all together to the minimum non-overlapping set
def calculate_merged_slices(prior_slices, current_slices):
    new_slices = prior_slices
    for current in current_slices:
        new_slices = merge_slice(new_slices, current)
    return new_slices


    # # merged_slices = []
    # # current_slices = []
    # # for unmerged in current_slices:
    # #     print(f"{unmerged=}")
    # #     if not merged_slices:
    # #         current_slices = [unmerged]
    # #     else:
    # #         while merged_slices:
    # #             merged = merged_slices.pop()
    # #             print(f"{merged=}")
    # #             print(f"Appending to {current_slices=}")
    # #             current_slices += merge_slice_pair(unmerged, merged)
    # #     print(f"Before apending new slices: {merged_slices=}")
    # #     print(f"New slices to append: {current_slices=}")
    # #     merged_slices += current_slices
    # #     print(f"After appending: {merged_slices=}")
    # #     current_slices.clear()
    # return merged_slices


# Given a pair of slices, find the new slice range if they overlap or the pair of slices if they don't
def merge_slice(slices, current):
    if not slices:
        return [current]

    c1, c2 = current
    for idx, (p1, p2) in enumerate(slices):
        # Additive cases
        if p1 == c2:
            return slices[:idx] + [(c1, p2)] + slices[idx + 1:]
        if p2 == c1:
            return slices[:idx] + [(p1, c2)] + slices[idx + 1:]

        # Expansive case
        if p1 == c1:
            return slices[:idx] + [(p1, max(p2, c2))] + slices[idx + 1:]
        if p2 == c2:
            return slices[:idx] + [(min(p1, c1), c2)] + slices[idx + 1:]


        # Non overlapping cases
        if c2 < p1 or c1 > p2:
            return slices + [(c1, c2)]

        # All other cases create no change from the prior list of slices.
        
    return slices


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
use_example = True
alt_input = ""
# alt_input = "day18_ex2.txt"
# alt_input = "day18_ex3.txt"
part2 = False
import textwrap

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, alt_input)

    # input_text = textwrap.dedent(
    #     """\
    #     U 2 ()
    #     R 1 ()
    #     D 1 ()
    #     R 1 ()
    #     D 1 ()
    #     L 2 ()
    #     """
    # )

    answer = process_input(input_text)
    print(answer)

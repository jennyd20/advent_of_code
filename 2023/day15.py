import lib
import re


def initialize_sequence(steps):
    # [[box0[lens0, focal0], [lens1, focal1]], [box1[]], [box2[l3, f3], [l4, f4], [l5, f5]]]
    LENS_BOXES = [[] for _ in range(256)]

    for x in steps:
        label, op, focal_len = re.split("(\W)", x)
        box_num = get_hash_value(label)

        box = LENS_BOXES[box_num]
        if op == "-":
            for x, lens in enumerate(box):
                # If it has the lens, remove it
                if lens[0] == label:
                    del box[x]
                    break
        elif op == "=":
            # Note: The initial problem specifies there will be no blank focal lengths when adding a lens
            # The lens exists.  Check if it is already in the box.
            for y, l in enumerate(box):
                if l[0] == label:
                    # If so, update to the new focal length
                    box[y][1] = focal_len
                    break
            else:
                # It isn't already in the box, so add it
                box.append([label, focal_len])
        else:
            raise ValueError(f"Invalid operation: {op}")

    # Calculate final value
    focusing_power = 0
    for z, box in enumerate(LENS_BOXES):
        # Don't care about the label any more, just want the focal length
        for j, (_, focal_len) in enumerate(box):
            focusing_power += (z + 1) * (j + 1) * int(focal_len)
    return focusing_power


# Increase by ASCII value, multiply by 17, mod 256
def get_hash_value(input):
    val = 0
    for s in input:
        val += ord(s)
        val *= 17
        val = val % 256
    return val


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part2 = True

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    input_list = input_text.split(",")

    if not part2:
        answer = sum(get_hash_value(input_str) for input_str in input_list)
    else:
        answer = initialize_sequence(input_list)
    print(answer)

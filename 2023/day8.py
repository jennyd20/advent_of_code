import lib
import math

DIR_TO_IDX = {"L": 0, "R": 1}


def parse_map(input_text):
    """Turn the lines of text into tuple containing a string of instructions and a dictionary where the key is the input node and the values are the options for left or right traversal"""
    inst, nodes_text = input_text.split("\n\n")
    nodes = nodes_text.splitlines()

    node_dict = {}
    for n in nodes:
        key, dest = n.split(" = ")
        # l_val, r_val = dest.split(", ")
        # vals = [l_val[1:], r_val[:-1]]
        vals = dest[1:-1].split(", ")
        node_dict[key] = vals

    # For instructions, can either just turn them into 0s or 1s here (as a number rather than a string)
    # Alternatively, have a global dictionary

    return inst, node_dict


def map_steps(input_text):
    instructions, node_dict = parse_map(input_text)

    # TODO: Set up so part 1 takes a list of a single start input, part 2 can pass in all start inputs.
    # For each list in start_list, track individual steps

    # Find the starting node and set up initial values
    if part1:
        # In part 1, we only have one node that we're starting with
        all_starts = ["AAA"]
    else:
        # In part 2, we have multiple starting nodes, so find all that end in "A"
        # all_starts = [x for x in node_dict.keys() if x[2] == "A"]
        all_starts = [x for x in node_dict if x[2] == "A"]
    # inst_idx = 0
    # Use mod on the num_steps rather than tracking separately

    all_step_counts = []
    for first_node in all_starts:
        all_step_counts.append(
            find_steps_to_end_from_node(instructions, first_node, node_dict)
        )

    return calculate_all_steps(all_step_counts)


def calculate_all_steps(step_list):
    if len(step_list) == 1:
        return step_list[0]
    # Calculate the least common factors
    return math.lcm(*step_list)


def find_steps_to_end_from_node(instructions, current_node, node_dict):
    max_inst = len(instructions)
    num_steps = 0
    # Put in a break so this loop will end eventually
    while num_steps < 10000000:
        inst_step = instructions[num_steps % len(instructions)]
        # print(f"Starting the loop at node: {current_node}, step is {inst_step}")
        # Check to see if we are at the end
        if (part1 and current_node == "ZZZ") or (current_node[2] == "Z"):
            return num_steps
        # Otherwise, Follow the instruction to the next node

        current_node = node_dict[current_node][DIR_TO_IDX[inst_step]]

        # left_or_right = node_dict[current_node]
        # match inst_step:
        #     case "L":
        #         current_node = left_or_right[0]
        #     case "R":
        #         current_node = left_or_right[1]
        #     case _:
        #         raise ValueError(f"Not a valid instruction {inst_step}")

        # print(f"After node: {current_node}")

        # Update the instruction, loop if at the end of the list
        # Use the mod on the steps instead
        # inst_idx = inst_idx + 1 if inst_idx < max_inst - 1 else 0
        num_steps += 1

    # Should not get to this code.
    raise RuntimeError(
        f"Never found the end, we're trapped forever after {num_steps} steps"
    )


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part1 = False
alt_input = None
# alt_input = "day8_ex2.txt"
# alt_input = "day8_ex3.txt"

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, alt_input)
    answer = map_steps(input_text)
    print(answer)

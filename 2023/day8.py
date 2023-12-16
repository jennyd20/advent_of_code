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
        vals = dest[1:-1].split(", ")
        node_dict[key] = vals

    return inst, node_dict


def map_steps(input_text, end_node, start_node_maker):
    instructions, node_dict = parse_map(input_text)
    all_starts = start_node_maker(node_dict)
    all_step_counts = []
    for first_node in all_starts:
        all_step_counts.append(
            find_steps_to_end_from_node(instructions, first_node, node_dict, end_node)
        )

    return math.lcm(*all_step_counts)


def find_steps_to_end_from_node(instructions, current_node, node_dict, end_node):
    num_steps = 0
    # Put in a break so this loop will end eventually
    while num_steps < 1000000000:
        inst_step = instructions[num_steps % len(instructions)]
        if end_node(current_node):
            return num_steps
        current_node = node_dict[current_node][DIR_TO_IDX[inst_step]]
        num_steps += 1

    # Should not get to this code.
    raise RuntimeError(
        f"Never found the end, we're trapped forever after {num_steps} steps"
    )


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part1 = True
alt_input = None
# alt_input = "day8_ex2.txt"
# alt_input = "day8_ex3.txt"

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, alt_input)
    if part1:
        end_node = lambda node: node == "ZZZ"
        start_node_maker = lambda node_dict: ["AAA"]
    else:
        end_node = lambda node: node[2] == "Z"
        start_node_maker = lambda node_dict: [x for x in node_dict if x[2] == "A"]

    answer = map_steps(input_text, end_node, start_node_maker)
    print(answer)

import lib


def parse_map(input_text):
    inst, nodes_text = input_text.split("\n\n")
    nodes = nodes_text.splitlines()

    node_dict = {}
    for n in nodes:
        key, dest = n.split(" = ")
        l_val, r_val = dest.split(", ")
        vals = [l_val[1:], r_val[:-1]]
        node_dict[key] = vals

    return inst, node_dict


def map_steps(input_text):
    inst, node_dict = parse_map(input_text)
    return 0


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = True
part1 = True
alt_input = None
# alt_input = "day8_ex2.txt"

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, alt_input)
    answer = map_steps(input_text)
    print(answer)

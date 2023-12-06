import lib


def process_part_numbers():
    # Assume that line lengths are consistent, so don't need to check on every line
    max_row = len(engine_diagram)
    max_cols = len(engine_diagram[0])

    sum_parts = 0
    sum_gear_ratio = 0

    # For each line in the engine, create a dictionary of numbers and their index in the line
    for row, line in enumerate(engine_diagram):
        line_dict = build_line_dict(line)

        # Part 1 calculation
        for i, num in line_dict.items():
            row_range = range(max(row - 1, 0), min(row + 2, max_row))
            # row_range2 = max(row - 1, 0), min(row + 2, max_row)
            col_range = range(max(i - 1, 0), min(i + len(num) + 1, max_cols))
            if valid_part_number(row_range, col_range, num):
                sum_parts += int(num)

    # Part 2 calculation
    for gear in valid_gears.values():
        if len(gear) == 2:
            sum_gear_ratio += int(gear[0]) * int(gear[1])

    return sum_parts, sum_gear_ratio


def build_line_dict(line):
    line_dict = {}
    current_num_idx = -1
    current_num = ""
    for i, chr in enumerate(line):
        if chr.isdigit():
            if current_num == "":
                current_num_idx = i
            current_num += chr
        else:
            if current_num_idx >= 0:
                line_dict[current_num_idx] = current_num
                current_num = ""
                current_num_idx = -1
    # Make sure to account for a number at the end of a line
    if current_num_idx >= 0:
        line_dict[current_num_idx] = current_num

    return line_dict


def valid_part_number(row_range, col_range, num):
    for row in row_range:  # start, end = range(*row_range2)
        # for row in range(*row_range):
        for col in col_range:
            chr = engine_diagram[row][col]
            # Not period or digit, so found a special character
            if chr != "." and not chr.isdigit():
                # Part 2: Populate the gear info here while we're already traversing the grid
                if chr == "*":
                    coords = (row, col)
                    old_value = valid_gears.get(coords)
                    if old_value:
                        valid_gears[coords].append(num)
                    else:
                        valid_gears[coords] = [num]
                return True

    # No special character found
    return False


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
engine_diagram = None
valid_gears = {}


if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    engine_diagram = input_text.splitlines()
    sum_parts, sum_gears = process_part_numbers()
    print("Part 1: " + str(sum_parts) + "\t\tPart 2: " + str(sum_gears))

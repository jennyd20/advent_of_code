# ☃
import lib

# Get the difference between each pair of numbers one at a time
# We now have n-1 numbers
# If they are not all zeroes, --recurse-- or iterate? and do it again
# Once they are all zeroes, add zero to the last number of the line above
# Continue adding this new number to the last number in the line above
# Return the value you get when you get to the original input line


def get_value_prediction(value_history_str):
    v_hist = [int(x) for x in value_history_str.split(" ")]

    edge_nums = []
    done = False
    current_line = v_hist

    while not done:
        next_line, edge_num = get_next_line(current_line)
        edge_nums.append(edge_num)
        current_line = next_line
        done = is_line_done(next_line)

    if part1:
        answer = sum(edge_nums)
    else:
        edge_nums.append(0)
        edge_nums.reverse()

        added_num = 0
        for i in range(len(edge_nums) - 1):
            added_num = edge_nums[i + 1] - added_num
        answer = added_num

    return answer


def get_next_line(line):
    next = []
    for i in range(len(line) - 1):
        diff = line[i + 1] - line[i]
        next.append(diff)
        edge_num = line[len(line) - 1] if part1 else line[0]
    return next, edge_num


def is_line_done(line):
    return all(x == 0 for x in line)


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part1 = False

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    answer = sum(get_value_prediction(line) for line in input_text.splitlines())
    print(answer)

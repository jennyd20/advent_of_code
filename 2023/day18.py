import lib


def process_plan(input_text):
    plan = []
    for row in input_text.splitlines():
        dir, dist, color = row.split(" ")
        plan.append([dir, int(dist), color])

    outline_dict = {}
    x_idx = 0
    y_initial_idx = 0
    y_final_idx = 0
    for line in plan:
        dir, dist, color = line

        # Set up a dictionary where each row (key) contains a list (value) of starting idx and length of any given run in that row
        # In the vertical case, need to add a single point at each x value in the range
        if dir in ("U", "D"):
            for i in range(dist - 1):
                offset = i + 1
                if dir == "U":
                    offset = -offset
                outline_dict.setdefault(x_idx + offset, []).append((y_initial_idx, 1))
            x_idx += dist if dir == "D" else -dist

        elif dir in ("L", "R"):
            y_final_idx = y_initial_idx + (dist if dir == "R" else -dist)
            y_lower = min(y_initial_idx, y_final_idx)
            outline_dict.setdefault(x_idx, []).append((y_lower, dist))

        else:
            raise ValueError("Nope")

        y_initial_idx = y_final_idx

    # TODO: right now there are off-by-one errors when going left/right after an up/down

    # End processing this line
    pass

    return outline_dict


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
example_or_other = True #"day18_ex2.txt"  
part2 = False

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input2(__file__, example_or_other)

    answer = process_plan(input_text)
    print(answer)


# Note: this has a lot in common with Day 10, with looping and finding the internal area of the loop.

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

        # match dir:
        #     case "U":
        #         for _ in range(dist):
        #             outline_dict.setdefault(x, []).append((x - 1, y))
        #             x -= 1
        #         pass
        #     case "D":
        #         for _ in range(dist):
        #             outline_dict.setdefault(x, []).append((x + 1, y))
        #             x += 1
        #         pass
        #     case "L":
        #         # Moving left from the start index - subtract to find the first index
        #         for _ in range(dist):
        #         outline_dict.setdefault(x, []).append((y - dist, y))
        #         y -= 1
        #         pass
        #     case "R":
        #         # Moving right from the start index - just take the start and end indices of the line
        #         endpoint = y + dist
        #         outline_dict.setdefault(x, []).append((y, endpoint))
        #         y = endpoint
        #         pass
        #     case _:
        #         raise ValueError("Invalid input!  Kablooie!")

        # match dir:
        #     case "U":
        #         x_idx -= dist
        #         pass
        #     case "D":
        #         x_idx += dist
        #         pass
        #     case "L":
        #         y_final_idx = y_initial_idx - dist
        #         pass
        #     case "R":
        #         y_final_idx = y_initial_idx + dist
        #         pass
        #     case _:
        #         raise ValueError("Invalid input!  Kablooie!")

        # # Need to set dict values for up/down cases
        # outline_dict.setdefault(x_idx, []).append(
        #     set(sorted((y_initial_idx, y_final_idx)))
        # )
        # y_initial_idx = y_final_idx
        # pass


        # TODO - BAD MATH
        if dir in ("U", "D"):
            for i in range(dist):
                if dir == "U":
                    i = -i
                outline_dict.setdefault(x_idx + i, []).append(
                    tuple(sorted((y_initial_idx, y_final_idx)))
                )
            # TODO - update the x_idx

        elif dir in ("L", "R"):
            y_final_idx = y_initial_idx + (dist if "R" else -dist)

        else:
            raise ValueError("Nope")

        outline_dict.setdefault(x_idx, []).append(
            tuple(sorted((y_initial_idx, y_final_idx)))
        )
        y_initial_idx = y_final_idx

    # End processing this line
    pass

    return outline_dict


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
example_or_other = True
part2 = False

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input2(__file__, example_or_other)

    answer = process_plan(input_text)
    print(answer)


# Note: this has a lot in common with Day 10, with looping and finding the internal area of the loop.

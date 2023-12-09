import lib
import functools
import operator


def parse_input(input):
    # Return a list of the race [time, record]
    record = input.splitlines()
    time_list = list(filter(None, record[0].split(" ")[1:]))
    record_list = list(filter(None, record[1].split(" ")[1:]))

    races = []
    if part1:
        for i in range(len(time_list)):
            races.append([int(time_list[i]), int(record_list[i])])
        return races
    # Create one ginormous race
    else:
        return [
            [
                int("".join([t for t in time_list])),
                int("".join([r for r in record_list])),
            ]
        ]


def find_margin(race):
    time, record = race
    dist = []
    for t in range(time):
        move_time = time - t
        d = move_time * t
        dist.append(d)

    # Find the element of the first thing that is greater than the record
    first_win = -1
    last_win = -1
    for i, d in enumerate(dist):
        if d > record:
            first_win = i
            break
    # Find the element of the last thing that is greater than the record
    for i, d in enumerate(reversed(dist)):
        if d > record:
            last_win = len(dist) - i
            break

    total = last_win - first_win

    return total


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part1 = False

if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    races = parse_input(input_text)
    # Multiply instead of sum, works for both parts 1 and 2
    print(functools.reduce(operator.mul, (find_margin(race) for race in races), 1))

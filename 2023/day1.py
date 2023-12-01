import lib


word_to_digit = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "zero": 0,
}


def get_digit(sub_line):
    start_char = sub_line[0]
    digit_char = ''
    # Check for digit
    if start_char.isdigit():
        digit_char = start_char

    # Check for word
    elif (part2):    
        for numword in word_to_digit:
            if sub_line.startswith(numword):
                digit_char = word_to_digit[numword]
                break
    return str(digit_char)


# Look for the first digit or numword, and then the last digit or numword
def cal_value(line):
    len_line = len(line)
    digit_char1 = ''
    digit_char2 = ''

    for i in range(0, len_line):
        if not (digit_char1 and digit_char2):
            # First digit or numword
            if not digit_char1:
                digit_char1 = get_digit(line[i:])
            # Last digit or numword
            if not digit_char2:
                digit_char2 = get_digit(line[(len_line - 1 - i ) :])
        else:
            break

    # Append them together into a single 2 digit number
    return int(digit_char1 + digit_char2)

### SCRIPT ARGUMENTS ###
use_example = False
part2 = False

if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    answer = sum(cal_value(line) for line in input_text.splitlines())
    print(answer)

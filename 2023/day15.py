import lib

def get_hash_value(input_str):
    val = 0
    for s in input_str:
        # Increase by ASCII value
        val += ord(s)
        # Multiply by 17
        val *= 17
        # Mod 256
        val = val % 256
    return val

### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part2 = False

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    
    answer = sum(get_hash_value(input_str) for input_str in input_text.split(","))
    print(answer)

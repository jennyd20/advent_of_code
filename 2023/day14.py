import lib

def north_beam_load(platform):
    # Roll all rocks to the north
    '''
    Start on north edge
    For each row beyond the north edge, if there's a blank space to the north or a rounded rock,
    go north until we hit the edge or a square rock.

    OR
    Start on the south edge
    Make groups of rocks that are collapsing down
    Count how many round rocks are between # delimited square rocks
    Then move that number to the edge or the square rock.
    '''
    height = len(platform)
    width = len(platform[0])
    total_strain = 0

    for i in range(width):
        # Generate each column of the platform
        col = ""
        for j in range(height):
            col += platform[j][i]

        # Collapse the rolling boulders to the north side
        # Start at the south side and collect groups of boulders ("O") until we find an edge or an unmoving rock
        
        # rock_group = None
        # for x in reversed(col):
        #     if x == "O":
        #         # Add this rock to the group
        #     elif x == ".":
        #         roll_rock = True
        #     else: # x == #
        
        tipped_col = ""
        rocks_in_group = 0
        ground_in_group = 0
        
        # The columns are now going to be represented as horizontal strings, with left being "north"
        for x in col:
            if x == "O":
                rocks_in_group += 1
            elif x == ".":
                ground_in_group += 1
            else: # x == "#"
                # Collect boulders into a group
                tipped_col += "O" * rocks_in_group
                tipped_col += "." * ground_in_group
                tipped_col += "#"
                rocks_in_group = 0
                ground_in_group = 0
        else:
            # When we reach the end of the column, make sure to add any rolled boulders from there
            tipped_col += "O" * rocks_in_group
            tipped_col += "." * ground_in_group
        
        print(tipped_col)
        # Calculate the strain of that column
        col_strain = 0
        for idx, y in enumerate(tipped_col):
            if y == "O":
                col_strain += height - idx
        total_strain += col_strain
    return total_strain

### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part2 = False

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    answer = north_beam_load(input_text.splitlines())
    print(answer)

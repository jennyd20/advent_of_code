import lib

# Limit memory usage so I don't burn down the house with an overheating processor
import resource

resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))


# TODO(Jenny)
# Will need to convert part1 to use [[seed1, 1], [seed2, 1], [seed3, 1]]
# For part two, need to use [[seed1, seedrange], [seed2, seedrange]]
# So, part 1 will use the same code but with range of 1 or everything


def process_seeds(almanac):
    # Split the almanac into sections
    al_sections = almanac.split("\n\n")

    # Get the initial seed data, which will always be on the first line
    ids = [int(a) for a in al_sections.pop(0).split(":")[1].strip().split(" ")]

    if not part1:
        # Get all seeds from ranges
        expanded_seeds = []
        seed_pairs = lib.split_list(ids, 2)
        for pair in seed_pairs:
            newlist = []
            expanded_seeds += [*range(pair[0], sum(pair))]
            ids = expanded_seeds

    # TODO(Jenny) - improvement / algorithm steps
    # Get a range of IDs
    # get the part that is in the map
    # find offset of this overlap
    # adjust values to mapped values
    # for everything not in the range, do not change anything

    # For each seed, find the mapped value of each of the subsequent sections
    for mapping in al_sections:
        map_lookup(mapping, ids)

    return min(ids)


def map_lookup(map, ids):
    lines = map.splitlines()[1:]  # First line describes the map, so skip that
    # Track values that have been updated
    completed_map = set()
    # TODO(Jenny): start with seeds instead of lines so I don't use extra cycles checking lines that aren't needed
    for line in lines:
        dest_start, src_start, range_len = [int(a) for a in line.split(" ")]
        for i, val in enumerate(ids):
            if not i in completed_map and src_start <= val < src_start + range_len:
                ids[i] = dest_start + (val - src_start)
                completed_map.add(i)
    # Don't need to return because I'm modifying the IDs in place


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part1 = True

if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    print(str(process_seeds(input_text)))

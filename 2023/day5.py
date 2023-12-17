import lib

# Limit memory usage so I don't burn down the house with an overheating processor
import resource

# resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))


def process_seeds(almanac):
    # Split the almanac into sections
    almanac_sections = almanac.split("\n\n")

    # Get the initial seed data, which will always be on the first line
    init_ids = [
        int(a) for a in almanac_sections.pop(0).split(":")[1].strip().split(" ")
    ]

    if part1:
        # In part 1, all ranges are 1
        all_ids_and_ranges = [[i, 1] for i in init_ids]

    else:
        # In part 2, the second in a pair is the range of the seed specified in the first of the pair
        all_ids_and_ranges = lib.split_list(init_ids, 2)

    # For each seed, find the mapped value of each of the subsequent sections
    for section in almanac_sections:
        all_ids_and_ranges = map_lookup(
            text_to_almanac_map(section), all_ids_and_ranges
        )

    answer = min(pair[0] for pair in all_ids_and_ranges)
    return answer


def text_to_almanac_map(section):
    lines = section.splitlines()[1:]  # First line describes the map, so skip that
    section_map = []
    for l in lines:
        dest_start, source_start, range_len = l.split(" ")
        section_map.append((int(dest_start), int(source_start), int(range_len)))
    return section_map


def map_one_range(map, id_range_pair):
    map_newdest_start, map_start, map_range_len = map
    map_past_end = map_start + map_range_len
    input_start, input_range_len = id_range_pair
    input_past_end = input_start + input_range_len

    if input_range_len < 0:
        raise ValueError("Negative range, something broke.")

    mapped = []
    unmapped = []
    # If the input start is lower than the mapping start...
    if input_start < map_start:
        if input_past_end < map_start:
            unmapped.append(id_range_pair)
        elif input_past_end <= map_past_end:
            unmapped.append([input_start, map_start - input_start])
            mapped.append([map_newdest_start, input_past_end - map_start])
        elif input_past_end > map_past_end:
            unmapped.append([input_start, map_start - input_start])
            unmapped.append([map_past_end, input_past_end - map_past_end])
            mapped.append([map_newdest_start, map_range_len])
        else:
            raise RuntimeError()

    # Else, input_start >= map_start (or math broke)
    else:
        if input_start >= map_past_end:
            unmapped.append(id_range_pair)
        elif input_past_end <= map_past_end:
            offset = input_start - map_start
            mapped.append([map_newdest_start + offset, input_range_len])
            pass
        elif input_past_end > map_past_end:
            offset = input_start - map_start
            mapped.append([map_newdest_start + offset, map_past_end - input_start])
            unmapped.append([map_past_end, input_past_end - map_past_end])
            pass
        else:
            raise RuntimeError()

    return mapped, unmapped


def map_lookup(map, all_ids_and_ranges):
    # Find the overlap between the id and id+range and the values in the map
    new_id_range_pairs = []
    for m in map:
        all_unmapped_ranges = []
        for id_range_pair in all_ids_and_ranges:
            mapped_range, unmapped_ranges = map_one_range(m, id_range_pair)

            all_unmapped_ranges.extend(unmapped_ranges)
            new_id_range_pairs.extend(mapped_range)

        all_ids_and_ranges = all_unmapped_ranges
    return new_id_range_pairs + all_unmapped_ranges


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part1 = False

if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    print(str(process_seeds(input_text)))

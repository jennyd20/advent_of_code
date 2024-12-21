def process_input(input_text):
    # Split the input into rules and updates
    r, u = input_text.split("\n\n")
    rules = [x.split("|") for x in r.splitlines()]
    updates = [y.split(",") for y in u.splitlines()]

    # For each update, check to see if it matches the rule
    mid_page_sum = 0
    for update in updates:
        applicable_rules = get_applicable_rules(update, rules)
        if is_ordered(update, applicable_rules):
            if part1:
                mid_page_sum += get_mid_page(update)
        elif not part1:
            fixed_update = fix_update(update, applicable_rules)
            mid_page_sum += get_mid_page(fixed_update)

    return mid_page_sum


def get_applicable_rules(update, rules):
    applicable_rules = []
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            applicable_rules.append(rule)

    return applicable_rules


def get_mid_page(update):
    mid_idx = len(update) // 2
    return int(update[mid_idx])


def get_num_idxs(update, rule):
    # *** This should never throw an error, since we've already removed the rules that
    # don't apply
    return update.index(rule[0]), update.index(rule[1])


def is_ordered(update, rules):
    for rule in rules:
        # For each rule, see if the update passes that rule
        idxs = get_num_idxs(update, rule)
        if idxs[0] > idxs[1]:
            return False

    return True


# Can make this more efficient by keeping track of which rule this broke on.
def fix_update(update, rules):
    # Make a dictionary of all numbers in the update with all the
    # numbers that should follow them
    ordering_dict = {x: [] for x in update}
    for r in rules:
        ordering_dict[r[0]].append(r[1])

    return _generate_list(ordering_dict)


# Find all the values that have no dependencies, add them to the end of the queue
# Then remove all references to them from the other dictionary value entries
# Recurse on the new updated dictionary


# *** Instead of using a stack with recursion, can use a while loop
def _generate_list(rule_map):
    fixed_update = []
    while rule_map:
        to_remove = []
        for k, v in rule_map.items():
            if not v:
                to_remove.append(k)
                fixed_update.insert(0, k)
        for k in to_remove:
            del rule_map[k]
        if to_remove:
            rule_map.update(
                (k, list(set(v) - set(to_remove))) for k, v in rule_map.items()
            )

    return fixed_update


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
import lib

part1 = False
use_example = False

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    answer = process_input(input_text)
    print(answer)

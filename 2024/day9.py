import dataclasses
import collections


###################### CUSTOM CLASSES ######################
@dataclasses.dataclass
class File:
    id: int
    size: int

    def __str__(self):
        # return f"|{self.id}|"*self.size
        return str(self.id) * self.size


@dataclasses.dataclass
class Space:
    size: int
    used: bool = False

    def __str__(self):
        c = "." if not self.used else ","
        return c * self.size


@dataclasses.dataclass
class Mydeque(collections.deque):
    def __str__(self):
        return "".join(list(map(str, list(self))))


def prettyprint(dq, pos_idx):
    print("`" * pos_idx, dq, sep="")


######################## MAIN LOGIC ########################
def process_input(disk_map: str, part1: bool) -> int:
    checksum = 0

    # Convert the map to a deque of File and Space objects
    disk_deque = parse_map(disk_map)

    # The index of the final position of a block after the map has been unwound
    block_pos = 0

    # Go through the queue, starting at the left side (index 0).
    while disk_deque:
        # prettyprint(disk_deque, block_pos)
        left_block = disk_deque.popleft()
        match left_block:

            # If a file, just add the checksum value
            case File(file_id, size):
                for _ in range(size):
                    checksum += block_pos * file_id
                    block_pos += 1

            # If there's a space, try to fill it in with file contents
            case Space(size):
                # If the deque changes, go back through the list
                if filled_space(disk_deque, left_block, part1):
                    continue

                # If the deque didn't change, this space can't be filled in.
                # Since spaces get skipped when calculating the checksum,
                # just update the block_pos for future checksum calculations.
                else:
                    block_pos += size

    return checksum


# This deque already has the space we're processing popped off the front.
# We will get the last file popped off the back shortly.
def filled_space(
    disk_deque: collections.deque[File | Space], space_block: Space, part1: bool
) -> bool:

    # If this particular block of space was previously occupied by a file,
    # it cannot have any other files moved to cover it.
    if space_block.used:
        return False

    # If there is no last file (because the deque is empty or only contains
    # space) then there's nothing to fill the space with.
    last_file = get_last_file(disk_deque)
    if last_file is None:
        return False

    # If the last file fits in the existing space (for both part 1 and part 2),
    # move the whole thing over (keeping space extra if it exists).
    if last_file.size <= space_block.size:
        new_space_size = space_block.size - last_file.size
        if new_space_size > 0:
            disk_deque.appendleft(Space(new_space_size))
        disk_deque.appendleft(last_file)

    # If the last file is larger than the available space,
    # then shenanigans ensue based on which part we're solving
    else:
        # For part 1 - move over as many file chunks as will fit.
        # If there's any extra space in the file, leave that part at the end
        # of the deque for future use.
        if part1:
            new_front_file = File(last_file.id, space_block.size)
            assert new_front_file.size > 0
            disk_deque.appendleft(new_front_file)

            new_last_file_size = last_file.size - space_block.size
            if new_last_file_size > 0:
                new_last_file = File(last_file.id, new_last_file_size)
                disk_deque.append(new_last_file)

        # If in part 2 and moving whole file blocks, at this point we've
        # already determined that the last block won't fit.  Look backwards
        # through the deque to find one that will.
        if not part1:
            moved = moved_file(disk_deque, space_block)
            # Re-add the last file back to the deque since it hasn't moved
            disk_deque.append(last_file)
            return moved

    # If we've gotten here, space has been filled and the deque has changed.
    return True


# Given a space of size space_block.size, walk backwards through the deque to find the next file that can fit the space.
def moved_file(disk_deque: collections.deque[File | Space], space: Space) -> bool:
    # print(f"Move fitting file: {disk_deque=}, {space_block=}")
    for i in range(len(disk_deque) - 1, -1, -1):
        block = disk_deque[i]

        # If we find a file object that will fit the space size, slot it in!
        if isinstance(block, File) and block.size <= space.size:
            # Replace the found spot with a blank space
            disk_deque[i] = Space(block.size, used=True)

            # If there's any space remaining after adding the file length, add it on for future use.
            # Note: Since this space would have been occupied by a file, mark it as "used" so that
            # future files can't slot into here.
            remaining_space_size = space.size - block.size
            if remaining_space_size > 0:
                disk_deque.appendleft(Space(remaining_space_size))

            # Add the found block to the front, thus filling in the space
            disk_deque.appendleft(block)
            return True
    return False


# Get the most right-hand file.  Ignore space blocks.  Return none if no files remain in the deque
def get_last_file(disk_deque: collections.deque[File | Space]) -> File | None:
    while disk_deque:
        last = disk_deque.pop()
        match last:
            case Space():
                continue
            case File():
                return last
    return None


# Turn the string input into a deque of Files and Spaces
def parse_map(disk_map: str) -> collections.deque[File | Space]:
    # if len(disk_map) % 2 == 1:
    #     disk_map += "0"
    disk_deque = Mydeque()
    file_idx = 0
    for i, v in enumerate(disk_map):
        size = int(v)
        if size == 0:
            continue
        # If the loop i is even, this is a file.
        if i % 2 == 0:
            # File lengths should never be 0
            assert size > 0
            disk_deque.append(File(file_idx, size))
            file_idx += 1
        else:
            disk_deque.append(Space(size))

    return disk_deque


########### SCRIPT ARGUMENTS AND EXECUTION ###########
from aoc_libs import lib


def main(part1=True, use_example=False):
    input_text = lib.read_input(__file__, use_example)
    return process_input(input_text, part1)


if __name__ == "__main__":
    print(main(part1=True, use_example=False))

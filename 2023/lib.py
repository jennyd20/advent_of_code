from pathlib import Path


# From a given dayX.py, find the corresponding input (or example input) in /input
# So, day1.py would load in the text from day1_input.txt (or day1_ex.txt)
def read_input(orig_p, is_ex=False):
    src_p = Path(orig_p)
    src_name = src_p.stem
    assert src_name.startswith("day"), "Can only read input on dayX files"
    input_name = src_name + ("_ex" if is_ex else "_input") + ".txt"
    input_p = Path(src_p.parent / "input" / input_name)

    return input_p.read_text()


# Divide a list into chunks of a discrete length
def split_list(lst, chunk_size):
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]

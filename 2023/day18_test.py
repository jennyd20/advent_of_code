import pytest
import textwrap
import day18


####################################################
# TESTING CALCULATING AREAS
####################################################


def test_calculate_one_slice_area():
    input = [(-2, 6)]
    result = day18.calculate_index_area(input)
    assert result == 9


def test_calculate_two_slice_areas():
    input = [(0, 2), (3, 4)]
    result = day18.calculate_index_area(input)
    assert result == 5


def test_calculate_four_slice_areas():
    input = [(0, 2), (4, 6), (8, 10), (10, 12)]
    result = day18.calculate_index_area(input)
    assert result == 12


#
#  XX
#  #.
#  XX
#
#  ^
#  Sliced columns counted separately
#
def test_calculate_prior_area_when_adjacent():
    input = [(0, 2)]
    result = day18.calculate_middle_area(input, 0, 1)
    assert result == 0


#
#  X#X
#  #.#
#  X#X
#   ^
#
def test_calculate_prior_area_simple():
    input = [(0, 2)]
    result = day18.calculate_middle_area(input, 0, 2)
    assert result == 3


####################################################
# TEST MERGING
####################################################


def test_calculate_merged_pair_adding_above():
    prior_slices = [(0, 1)]
    curent_slice = (-1, 0)
    result = day18.merge_slice(prior_slices, curent_slice)
    expected = [(-1, 1)]
    assert sorted(result) == sorted(expected)


def test_calculate_merged_pair_adding_below():
    prior_slices = [(0, 4)]
    curent_slice = (-1, 0)
    result = day18.merge_slice(prior_slices, curent_slice)
    expected = [(-1, 4)]
    assert sorted(result) == sorted(expected)


def test_calculate_merged_pair_nonoverlapping():
    prior_slices = [(0, 1)]
    curent_slice = (-3, -4)
    result = day18.merge_slice(prior_slices, curent_slice)
    expected = [(-3, -4), (0, 1)]
    assert sorted(result) == sorted(expected)


# def test_merge_slices_single():
#     current_slices = [(-1, 1)]
#     result = day18.calculate_merged_slices(current_slices)
#     expected = [(-1, 1)]
#     assert sorted(result) == sorted(expected)


# #
# #    X   6
# #    #
# #    #
# #    X   3
# #
# #  X    1
# #  #
# #  X   -1
# #
# def test_merge_slices_separated():
#     current_slices = [(-1, 1), (3, 6)]
#     result = day18.calculate_merged_slices(current_slices)
#     expected = [(-1, 1), (3, 6)]
#     assert sorted(result) == sorted(expected)


# #
# #  X   5
# #  #
# #  #
# #  X  X  2
# #     #
# #     #
# #     X  -1
# #
# def test_merge_slices_overlapping_bottom():
#     current_slices = [(2, 5), (-1, 2)]
#     result = day18.calculate_merged_slices(current_slices)
#     expected = [(-1, 5)]
#     assert sorted(result) == sorted(expected)


# #
# #     X  22
# #     #
# #     #
# #  X  X  19
# #  #
# #  #
# #  X  16
# #
# def test_merge_slices_overlapping_top():
#     current_slices = [(16, 19), (19, 22)]
#     result = day18.calculate_merged_slices(current_slices)
#     expected = [(16, 22)]
#     assert sorted(result) == sorted(expected)


# ####################################################
# # TESTING CREATING NEW SLICES
# ####################################################

# def test_get_slice_union_one_input():
#     prior_slice = ()
#     current_slice = (0, 1)
#     with pytest.raises(AssertionError):
#         day18.get_slice_union(prior_slice, current_slice)


# def test_get_slice_union_not_overlapping():
#     prior_slice = (0, 1)
#     current_slice = (3, 5)
#     result = day18.get_slice_union(prior_slice, current_slice)
#     expected = [(0, 1), (3, 5)]
#     assert result == expected


# def test_get_slice_union_overlapping():
#     prior_slice = (0, 3)
#     current_slice = (2, 3)
#     result = day18.get_slice_union(prior_slice, current_slice)
#     expected = [(2, 3)]
#     assert result == expected

# def test_calculate_new_slices_single_input():
#     prior_slices = []
#     new_slices = [(0, 1)]
#     result = day18.calculate_next_slices(prior_slices, new_slices)
#     expected = [(0, 1)]
#     assert result == expected

# def test_calculate_new_slices_non_overlapping():
#     prior_slices = [(3, 4)]
#     new_slices = [(0, 1)]
#     result = day18.calculate_next_slices(prior_slices, new_slices)
#     expected = [(0, 1), (3, 4)]
#     assert result == expected


# ####################################################
# # TESTING PROCESS SLICE
# ####################################################


# #
# #  X
# #  #
# #  X
# #
# def test_initial_process_slice():
#     x_idx = -1
#     x_slices = [(0, 2)]
#     prior_idx = 0
#     prior_slices = []
#     new_area, new_slices = day18.process_slices(x_idx, x_slices, prior_idx, prior_slices)
#     assert new_area == 3
#     assert new_slices == [(0, 2)]


# #
# #  X#X  2
# #  #.#
# #  X#X  0
# #
# #  0 2
# #

# def test_second_idx_process_slices():
#     x_idx = 2
#     x_slices = [(0, 2)]
#     prior_idx = 0
#     prior_slices = [(0, 2)]
#     new_area, new_slices = day18.process_slices(x_idx, x_slices, prior_idx, prior_slices)
#     assert new_area == 6
#     assert new_slices == [(0, 2)]


# ####################################################
# # WARNING: UNSORTED MESS BELOW
# ####################################################

# """
# X
# #
# X

# """

# def test_initial_single_process_slices():
#     x_idx = -1
#     x_slices = [(0, 2)]
#     prior_idx = 0
#     prior_slices = []
#     new_area, new_slices = day18.process_slices(x_idx, x_slices, prior_idx, prior_slices)
#     assert new_area == 3
#     assert new_slices == [(0, 2)]


# """
# X#X
# #.#
# X#X

# """

# def test_second_single_process_slices():
#     x_idx = 2
#     x_slices = [(0, 2)]
#     prior_idx = 0
#     prior_slices = [(0, 2)]
#     new_area, new_slices = day18.process_slices(x_idx, x_slices, prior_idx, prior_slices)
#     assert new_area == 6
#     assert new_slices == [(0, 2)]


# """

# ###X   1
# ...#   0
# ...#  -1
# ..XX  -2
# ..#   -3
# ##X   -4
#   ^

# """


# def test_calculate_prior_idx_slice_area_jigged_up():
#     input = [(-4, -2)]
#     result = day18.calculate_prior_idx_slice_area(input, -4, 1)
#     assert result == 6map


# """

# X##  10
# X##  9
#   #
# X##  7
# #..
# X##  5
#   #
# X##  3
# #..
# #..
# X##  0

# """


# def test_calculate_prior_idx_slice_area_out_edges():
#     input = [(0, 3), (5, 7), (9, 10)]
#     result = day18.calculate_prior_idx_slice_area(input, 0, 10)
#     assert result == 9


# """

#   ###  12
# ###.   11
# ....
# ....
# ###.   8
#   #.   7
#   ###  6
# """


# def test_calculate_prior_idx_slice_area_outie():
#     input = [(6, 8), (11, 12)]
#     result = day18.calculate_prior_idx_slice_area(input, 6, 12)
#     assert result == 7

# """

# X### >>    4
# X##X >>    3
# ...#       2
# ...#       1
# X##X       0
# #... >>   -1
# X### >>   -2

# -3 0

# """

# ####################################################
# # TESTING PROCESS SLICE
# ####################################################


# ###X   1
# ...#   0
# ...#  -1
# ..XX  -2
# ..#   -3
# ##X   -4
#   ^

# """


# """

# X##  10
# X##  9
#   #
# X##  7
# #..
# X##  5
#   #
# X##  3

####################################################
# TESTING FULL GRAPHS
####################################################
"""
Note about diagrams:
S = starting position
X = corner
# = edges
. = interior position
"""

####################################################
"""

SX
XX

"""


def test_small_square():
    # Start in upper left corner, clockwise
    input = textwrap.dedent(
        """\
        R 1 ()
        D 1 ()
        L 1 ()
        U 1 ()
        """
    )
    total = day18.process_input(input)
    assert total == 4


####################################################
"""

X#X
#.#
X#S

"""


def test_big_square():
    # Start in lower right corner, counter clockwise
    input = textwrap.dedent(
        """\
        U 2 ()
        L 2 ()
        D 2 ()
        R 2 ()
        """
    )
    total = day18.process_input(input)
    assert total == 9


####################################################
"""

X##X
#..#
#..#
S##X

"""


def test_bigger_square():
    # Start in lower left corner, clockwise
    input = textwrap.dedent(
        """\
        U 3 ()
        R 3 ()
        D 3 ()
        L 3 ()
        """
    )
    total = day18.process_input(input)
    assert total == 16


####################################################
"""

SX
##
XX

"""


def test_small_rectangle():
    # Start in upper left corner, clockwise
    input = textwrap.dedent(
        """\
        R 1 ()
        D 2 ()
        L 1 ()
        U 2 ()
        """
    )
    total = day18.process_input(input)
    assert total == 6


####################################################
"""

X###S
#   #
X###X

"""


def test_big_rectangle():
    # Start in upper right corner, clockwise
    input = textwrap.dedent(
        """\
        D 2 ()
        L 4 ()
        U 2 ()
        R 4 ()
        """
    )
    total = day18.process_input(input)
    assert total == 15


####################################################
"""

S###X   0
#   #   -1
#   #   -2
#   #   -3
#   #   -4
X###X   -5

0   4

"""


def test_bigger_rectangle():
    # Start in upper left corner, counter clockwise
    input = textwrap.dedent(
        """\
        D 5 ()
        R 4 ()
        U 5 ()
        L 4 ()
        """
    )
    total = day18.process_input(input)
    assert total == 30


####################################################
"""
Start on right corner, go clockwise around

 XX     1
 #XS    0
 X#X    -1

-2 0

"""


def test_simple_zig_bottom_right():
    # Start mid right, clockwise
    input = textwrap.dedent(
        """\
        D 1 ()
        L 2 ()
        U 2 ()
        R 1 ()
        D 1 ()
        R 1 ()
        """
    )
    total = day18.process_input(input)
    assert total == 8


"""


 X##X    1
 #..XS   0
 #...#  -1
 X###X  -2

"""
def test_larger_zig_bottom_right():
    # Start mid right, clockwise
    input = textwrap.dedent(
        """\
        D 2 ()
        L 4 ()
        U 3 ()
        R 3 ()
        D 1 ()
        R 1 ()
        """
    )
    total = day18.process_input(input)
    assert total == 19


def test_calculate_next_slices():
    prior_slices = [(-2, 1)]
    current_slices = [(0, 1)]
    expected = [(-2, 0)]
    result = day18.calculate_next_slices(prior_slices, current_slices)
    assert result == expected
####################################################
"""

  XX  2
 XX#  1
 S#X  0

 0 2

"""


def test_simple_zig_left():
    # Start mid right, clockwise
    input = textwrap.dedent(
        """\
        U 1 ()
        R 1 ()
        U 1 ()
        R 1 ()
        D 2 ()
        L 2 ()
        """
    )
    total = day18.process_input(input)
    assert total == 8


####################################################

# """


# X###X
# X#X #
#   # #
#   # #
# X#X #
# S###X

# """


# def test_u_zig_left():
#     # Start mid right, clockwise
#     input = textwrap.dedent(
#         """\
#         R 4 ()
#         U 5 ()
#         L 4 ()
#         D 1 ()
#         R 2 ()
#         D 3 ()
#         L 2 ()
#         D 1 ()
#         """
#     )
#     total, map = day18.process_input(input)
#     assert total == 26


# ####################################################

# """

#     X###X
#     #   #
#  S##X   #
#  #      #
#  #      #
#  X##X   #
#     x###x

# area = 8*7 - 9 = 47
# """


# def test_outie_left():
#     # Start mid right, clockwise
#     input = textwrap.dedent(
#         """\
#         R 3 ()
#         U 2 ()
#         R 4 ()
#         D 6 ()
#         L 4 ()
#         U 1 ()
#         L 3 ()
#         U 3 ()
#         """
#     )
#     total, map = day18.process_input(input)
#     assert total == 47


if __name__ == "__main__":
    pytest.main()

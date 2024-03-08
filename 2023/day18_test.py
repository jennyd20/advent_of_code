import pytest
import textwrap
import day18


####################################################
# TESTING CALCULATING AREAS
####################################################


def test_calculate_one_slice_area():
    input = [(-2, 6)]
    result = day18.calculate_column_area(input)
    assert result == 9


def test_calculate_two_slice_areas():
    input = [(0, 2), (3, 4)]
    result = day18.calculate_column_area(input)
    assert result == 5


def test_calculate_four_slice_areas():
    input = [(0, 2), (4, 6), (8, 10), (10, 12)]
    result = day18.calculate_column_area(input)
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
    result = day18.calculate_area_between_indices(input, 0, 1)
    assert result == 0


#
#  X#X
#  #.#
#  X#X
#   ^
#
def test_calculate_prior_area_simple():
    input = [(0, 2)]
    result = day18.calculate_area_between_indices(input, 0, 2)
    assert result == 3


####################################################
# TEST MERGING
####################################################


def test_calculate_merged_pair_adding_above():
    prior_slices = [(0, 1)]
    curent_slices = [(-1, 0)]
    result = day18.merge_slices(prior_slices, curent_slices)
    expected = [(-1, 1)]
    assert sorted(result) == sorted(expected)


def test_calculate_merged_pair_adding_below():
    prior_slices = [(0, 4)]
    curent_slices = [(-1, 0)]
    result = day18.merge_slices(prior_slices, curent_slices)
    expected = [(-1, 4)]
    assert sorted(result) == sorted(expected)


def test_calculate_merged_pair_nonoverlapping():
    prior_slices = [(0, 1)]
    curent_slices = [(-3, -4)]
    result = day18.merge_slices(prior_slices, curent_slices)
    expected = [(-3, -4), (0, 1)]
    assert sorted(result) == sorted(expected)


def test_merge_multiples_with_multiples():
    prior_slices = [(-7, -5), (-2, 0)]
    new_slices = [(-9, -5), (-2, 0)]
    result = day18.merge_slices(prior_slices, new_slices)
    expected = [(-9, -5), (-2, 0)]
    assert sorted(result) == sorted(expected)


def test_merge_two_into_three():
    prior_slices = [(-86, 33), (69, 106), (113, 137)]
    new_slices = [(-86, 33), (69, 106), (118, 130)]
    result = day18.merge_slices(prior_slices, new_slices)
    expected = [(-86, 33), (69, 106), (113, 137)]
    assert result == expected


def test_overlapping_merge():
    prior_slices = [(168, 180), (187, 191)]
    new_slices = [(168, 196)]
    result = day18.merge_slices(prior_slices, new_slices)
    assert result == [(168, 196)]


####################################################
# TESTING COLOR TO INSTRUCTION
####################################################


def test_convert_color_to_instruction_simple():
    color = "(#8ceee2)"
    dir, dist = day18.convert_color_to_instruction(color)
    assert dist == 577262
    assert dir == "L"


def test_get_plan_part_2():
    input = textwrap.dedent(
        """\
        X X (#000032)
        """
    )
    result = day18.get_plan_from_input(input, True)
    expected = [["L", 3]]
    assert result == expected


def test_testinput_plan_part_2():
    input = textwrap.dedent(
        """\
        X X (#70c710)
        X X (#0dc571)
        X X (#5713f0)
        X X (#d2c081)
        X X (#59c680)
        X X (#411b91)
        X X (#8ceee2)
        X X (#caa173)
        X X (#1b58a2)
        X X (#caa171)
        X X (#7807d2)
        X X (#a77fa3)
        X X (#015232)
        X X (#7a21e3)
        """
    )
    result = day18.get_plan_from_input(input, True)
    expected = [
        ["R", 461937],
        ["D", 56407],
        ["R", 356671],
        ["D", 863240],
        ["R", 367720],
        ["D", 266681],
        ["L", 577262],
        ["U", 829975],
        ["L", 112010],
        ["D", 829975],
        ["L", 491645],
        ["U", 686074],
        ["L", 5411],
        ["U", 500254],
    ]
    assert result == expected


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


"""
 X###X
 #...#
 X#X #
   # #
   X#X

"""


def test_zig_top_left():
    # Start mid right, clockwise
    input = textwrap.dedent(
        """\
        U 2 ()
        R 4 ()
        D 4 ()
        L 2 ()
        U 2 ()
        L 2 ()
        """
    )
    total = day18.process_input(input)
    assert total == 21


"""
   X#X
   #.#
 X#X #
 #   #
 X###X

"""


def test_zig_bottom_left():
    # Start mid right, clockwise
    input = textwrap.dedent(
        """\
        U 2 ()
        R 2 ()
        U 2 ()
        R 2 ()
        D 4 ()
        L 4 ()
        """
    )
    total = day18.process_input(input)
    assert total == 21


def test_calculate_next_slices():
    prior_slices = [(-2, 1)]
    current_slices = [(0, 1)]
    expected = [(-2, 0)]
    result = day18.generate_next_slices(prior_slices, current_slices)
    assert result == expected


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


"""


X###X
#   #
X#X #
  # #
  # #
X#X #
#   #
S###X

"""


def test_u_left():
    # Start mid right, clockwise
    input = textwrap.dedent(
        """\
        R 4 ()
        U 7 ()
        L 4 ()
        D 2 ()
        R 2 ()
        D 3 ()
        L 2 ()
        D 2 ()
        """
    )
    total = day18.process_input(input)
    assert total == 36


"""


X###X
#   #
# X#X
# #
# X#X
#   #
S###X

"""


def test_u_right_side():
    # Start mid right, clockwise
    input = textwrap.dedent(
        """\
        U 6 ()
        R 4 ()
        C 2 ()
        L 2 ()
        D 2 ()
        R 2 ()
        D 2 ()
        L 4 ()
        """
    )
    total = day18.process_input(input)
    assert total == 33


"""

   X#X
   # #
 X#X #
 #   #
 X#X #
   # #
   X#X

area = 6*2 + 15 = 27
"""


def test_simple_outie_left():
    # Start mid right, clockwise
    input = textwrap.dedent(
        """\
        R 2 ()
        U 2 ()
        R 2 ()
        D 6 ()
        L 2 ()
        U 2 ()
        L 2 ()
        U 2 ()
        """
    )
    total = day18.process_input(input)
    assert total == 27


"""

    X###X
    #   #
 S##X   #
 #      #
 #      #
 X##X   #
    x###x

area = 8*7 - 9 = 47
"""


def test_complex_outie_left():
    # Start mid right, clockwise
    input = textwrap.dedent(
        """\
        R 3 ()
        U 2 ()
        R 4 ()
        D 6 ()
        L 4 ()
        U 1 ()
        L 3 ()
        U 3 ()
        """
    )
    total = day18.process_input(input)
    assert total == 47


"""

   X#X
   # #
   # X#X
   #   #
   # X#X
   # #
   X#X

area = 6*2 + 15 = 27
"""


def test_simple_outie_right():
    input = textwrap.dedent(
        """\
        R 2 ()
        U 2 ()
        R 2 ()
        D 6 ()
        L 2 ()
        U 2 ()
        L 2 ()
        U 2 ()
        """
    )
    total = day18.process_input(input)
    assert total == 27


"""

      X#####X  10
      #     #  9
      X##X  #  8
         #  #  7
  X###X  #  #  6
  #   #  #  #  5
  # X#X  #  #  4
  # #    #  #  3
  # X####X  #  2
  #         #  1
  X#########X  0

  0 2 4  7  10

  Total area
  0: 7
    * Mid = 0
    * Column = 7
  2: +14 = 21
    * Mid = 7
    * Column = 7
  4: +15 = 36
    * Mid = 6
    * Column = 9
  7: + 23 = 59
    * Mid = 12
    * Column = 11
  10: + 33 = 92
    * Mid = 2 x 11 = 22
    * Column = 11

"""


def test_spiral():
    input = textwrap.dedent(
        """\
        U 6 ()
        R 4 ()
        D 2 ()
        L 2 ()
        D 2 ()
        R 5 ()
        U 6 ()
        L 3 ()
        U 2 ()
        R 6 ()
        D 10 ()
        L 10 ()
        """
    )
    total = day18.process_input(input)
    assert total == 92


def test_ending_slice_with_starting_with_middle():
    prior_slices = [(0, 2), (4, 6)]
    current_slices = [(4, 6), (8, 10)]
    new_slices = day18.generate_next_slices(prior_slices, current_slices)
    assert new_slices == [(0, 2), (8, 10)]
    merged_slices = day18.merge_slices(prior_slices, new_slices)
    assert merged_slices == [(0, 2), (4, 6), (8, 10)]


####################################################


if __name__ == "__main__":
    pytest.main()

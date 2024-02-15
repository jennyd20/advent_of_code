import pytest
import textwrap

import lib

import day18


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
    total, map = day18.process_input(input)
    assert map == [(0, -1), (0, 0), (1, -1), (1, 0)]
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
    total, map = day18.process_input(input)
    assert map == [(-2, 0), (-2, 2), (0, 0), (0, 2)]
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
    total, map = day18.process_input(input)
    assert map == [(0, 0), (0, 3), (3, 0), (3, 3)]
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
    total, map = day18.process_input(input)
    assert map == [(0, -2), (0, 0), (1, -2), (1, 0)]
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
    total, map = day18.process_input(input)
    assert map == [(-4, -2), (-4, 0), (0, -2), (0, 0)]
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
    total, map = day18.process_input(input)
    assert map == [(0, -5), (0, 0), (4, -5), (4, 0)]
    assert total == 30



"""
 XX     1
 #XS    0
 X#X    -1
 
-2 0
"""

def test_simple_zig():
    # Start mid right, clockwise
    input = textwrap.dedent(
        """\
        D 1 ()
        L 2 ()
        U 2 ()
        R 1 ()
        D 1 ()
        R 1 ()
        """)
    total, map = day18.process_input(input)
    assert map == [(-2, -1), (-2, 1), (-1, 0), (-1, 1), (0, -1), (0, 0)]
    assert total == 8



# def sort_border_dict(d):
#     for list_of_pairs in d.values():
#         list_of_pairs.sort()


# """
# ##
# S#
# ##
# """


# def test_rectangle_upper_mid_edge_start():
#     input = textwrap.dedent(
#         """\
#         U 1 ()
#         R 1 ()f test_easy_rectangle():
#     input = textwrap.dedent(
#         """\
#         R 1 ()
#         D 2 ()
#         L 1 ()
#         U 1 ()"""
#     )

#     total, dict = day18.process_input(input)
#     expected_dict = {-1: [(0, 2)], 0: [(0, 1), (1, 1)], 1: [(0, 2)]}
#     sort_border_dict(dict)
#     assert dict == expected_dict
#     assert total == 6


# """
# ##
# ##
# S#
# ##
# """


#         D 2 ()
#         L 1 ()
# def test_rectangle_lower_mid_edge_start():
#     input = textwrap.dedent(
#         """\
#         U 2 ()
#         R 1 ()
#         D 3 ()
#         L 1 ()
#         U 1 ()"""
#     )

#     total, dict = day18.process_input(input)
#     expected_dict = {
#         -2: [(0, 2)],
#         -1: [(1, 1), (0, 1)],
#         0: [(1, 1), (0, 1)],
#         1: [(0, 2)],
#     }
#     # assert dict == expected_dict
#     assert total == 8


# """

# x##x.   row 0   (line_area=4  total_area=0)            "####."
# ####.
# ####.
# xx#xx   row 3   (total_area += line_area * (3-1 - 0))  "####." "xx xx" -> ".####"
#  ####
#  ####
#  ####
#  x##x


#  x  x   row 8

# ####    x1
# #  #    x2
# ## ##   x1
#  #  #   x3
#  ####   x1

# """


# def test_find_total():
#     # 4 by 4, with empty space in the middle
#     input = textwrap.dedent(
#         """\
#         R 3 ()
#         D 3 ()
#         L 3 ()
#         U 3 ()"""
#     )
#     expected_dict = {
#         0: [(0, 1), (0, 4)],
#         1: [(0, 1), (3, 1)],
#         2: [(0, 1), (3, 1)],
#         3: [(0, 4)],
#     }
#     total, dict = day18.process_input(expected_dict)
#     assert dict == expected_dict
#     assert total == 16


# def test_find_total_backwards():
#     # 4 by 4, with empty space in the middle
#     input = textwrap.dedent(
#         """\
#         L 3 ()
#         U 3 ()
#         R 3 ()
#         D 3 ()"""
#     )
#     expected_dict = {
#         0: [(0, 1), (0, 4)],
#         1: [(0, 1), (3, 1)],
#         2: [(0, 1), (3, 1)],
#         3: [(0, 4)],
#     }
#     total, dict = day18.process_input(expected_dict)
#     # assert dict == expected_dict
#     assert total == 16


# def test_examples():
#     # input_text = lib.read_input(day18.__file__, False, "day18_ex2.txt")
#     # answer = day18.process_plan(input_text)
#     # assert answer == 123

#     tests = [
#         (
#             "day18_ex2.txt",
#             (
#                 16,
#                 {
#                     0: [(-3, 4)],
#                     -1: [(-3, 1), (0, 1)],
#                     -2: [(-3, 1), (0, 1)],
#                     -3: [(-3, 4)],
#                 },
#             ),
#         ),
#         (
#             "day18_ex3.txt",
#             (
#                 24,
#                 {
#                     -1: [(0, 1), (-1, 1), (2, 2), (1, 1)],
#                     -2: [(-1, 2), (1, 2)],
#                     0: [(-1, 1), (3, 1), (0, 2)],
#                     1: [(-1, 1), (1, 2), (3, 1)],
#                     2: [(-1, 3), (2, 2)],
#                 },
#             ),
#         ),
#         # ("day18_ex4.txt", (24, {-1: []})),
#         ("day18_ex5.txt", (8, {-1: [(0, 2)], 0: [(0, 1), (1, 2)], 1: [(0, 3)]})),
#     ]

#     for input_file, expected_answer in tests:
#         input_text = lib.read_input(day18.__file__, False, input_file)
#         answer = day18.process_input(input_text)
#         total, dict = answer
#         assert answer[0] == expected_answer[0]


# def test_ex5():
#     input_text = lib.read_input(day18.__file__, False, "day18_ex5.txt")
#     plan = day18.create_plan(input_text)
#     assert plan == [
#         ["U", 1, "()"],
#         ["R", 1, "()"],
#         ["D", 1, "()"],
#         ["R", 1, "()"],
#         ["D", 1, "()"],
#         ["L", 2, "()"],
#         ["U", 1, "()"],
#     ]
#     dict = day18.get_corner_coords_map(plan)
#     # assert dict == {-1: [(0, 2)], 0: [(0, 1), (1, 2)], 1: [(0, 3)]}
#     total = day18.find_area(dict)
#     assert total == 8


if __name__ == "__main__":
    pytest.main()

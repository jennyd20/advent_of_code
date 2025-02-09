import pytest
from aoc_libs.grid import Position
from aoc_libs.grid import Grid
import textwrap

import day10


def test_simple():
    input = "0123456789"
    assert day10.process_input(input) == 1


def test_one_trailhead_two_summits():
    # ...0...
    # ...1...
    # ...2...
    # 6543456
    # 7.....7
    # 8.....8
    # 9.....9

    input = textwrap.dedent(
        """\
    FFF0FFF
    FFF1FFF
    FFF2FFF
    6543456
    7FFFFF7
    8FFFFF8
    9FFFFF9
    """
    )

    assert day10.process_input(input) == 2


def test_one_trailhead_four_splitting_summits():
    # ..90..9
    # ...1.98
    # ...2..7
    # 6543456
    # 765.987
    # 876....
    # 987....

    input = textwrap.dedent(
        """\
    FF90FF9
    FFF1F98
    FFF2FF7
    6543456
    765F987
    876FFFF
    987FFFF
    """
    )

    assert day10.process_input(input) == 4


def test_two_trailheads():
    # 10..9..
    # 2...8..
    # 3...7..
    # 4567654
    # ...8..3
    # ...9..2
    # .....01

    input = textwrap.dedent(
        """\
    10FF9FF
    2FFF8FF
    3FFF7FF
    4567654
    FFF8FF3
    FFF9FF2
    FFFFF01
    """
    )

    assert day10.process_input(input) == 3


def test_part2_example_input():
    # 89010123
    # 78121874
    # 87430965
    # 96549874
    # 45678903
    # 32019012
    # 01329801
    # 10456732

    input = textwrap.dedent(
        """\
    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    """
    )

    assert day10.process_input(input) == 36


def test_part2_single_trailhead_few_trails():
    # .....0.
    # ..4321.
    # ..5..2.
    # ..6543.
    # ..7..4.
    # ..8765.
    # ..9....

    input = textwrap.dedent(
        """\
    FFFFF0F
    FF4321F
    FF5FF2F
    FF6543F
    FF7FF4F
    FF8765F
    FF9FFFF
    """
    )
    assert day10.process_input(input, part1=False) == 3


def test_part2_single_trailhead_some_trails():
    # ..90..9
    # ...1.98
    # ...2..7
    # 6543456
    # 765.987
    # 876....
    # 987....

    input = textwrap.dedent(
        """\
    FF90FF9
    FFF1F98
    FFF2FF7
    6543456
    765F987
    876FFFF
    987FFFF
    """
    )
    assert day10.process_input(input, part1=False) == 13


def test_part2_single_trailhead_many_trails():
    # 012345
    # 123456
    # 234567
    # 345678
    # 4.6789
    # 56789.

    input = textwrap.dedent(
        """\
    012345
    123456
    234567
    345678
    4F6789
    56789F
    """
    )
    assert day10.process_input(input, part1=False) == 227


def test_part2_example_input():
    # 89010123
    # 78121874
    # 87430965
    # 96549874
    # 45678903
    # 32019012
    # 01329801
    # 10456732

    input = textwrap.dedent(
        """\
    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    """
    )

    assert day10.process_input(input, part1=False) == 81

import pytest

import day1
import day2
import day3
import day4
import day5
import day6
import day7
import day8
import day9

# import dataclasses

# @dataclasses.dataclass
# class TestCase:
#     part1: bool
#     use_example: bool
#     expected_value: int

# # (part1, use_example), in order
# CASES = [
#     (True, True),
#     (True, False),
#     (False, True),
#     (False, False),
# ]

# DAYS = [
#     (day1, (11, 1506483, 31, 23126924))
# ]

# def test_all_days():
#     for day, cases in DAYS:
#         for (part1, use_example), expected_value in zip(CASES, cases):
#             assert day.main(part1=part1, use_example=use_example) == expected_value


# def run_cases(day, cases: list[TestCase]):
#     for case in cases:
#         assert day.main(part1=case.part1, use_example=case.use_example) == case.expected_value

# @pytest.mark.parametrize("part1,use_example,expected", [(True, True, 11),(True, False, 1506483)])
# def test_day1_variant(part1, use_example, expected):
#     assert day1.main(part1=part1, use_example=use_example) == expected

# def test_day1_variant2():
#     run_cases(day1, DAY1)


def test_day1():
    day = day1
    assert day.main(part1=True, use_example=True) == 11, "Test: True, True"
    assert day.main(part1=True, use_example=False) == 1506483, "Test: True, False"
    assert day.main(part1=False, use_example=True) == 31, "Test: False, True"
    assert day.main(part1=False, use_example=False) == 23126924, "Test: False, False"
    assert day.main(part1=False, use_example=False) == 44, "Test: True, True"


def test_day2():
    day = day2
    assert day.main(part1=True, use_example=True) == 2, "Test: True, True"
    assert day.main(part1=True, use_example=False) == 479, "Test: True, False"
    assert day.main(part1=False, use_example=True) == 4, "Test: False, True"
    assert day.main(part1=False, use_example=False) == 531, "Test: False, False"


def test_day3():
    day = day3
    assert day.main(part1=True, use_example=True) == 161, "Test: True, True"
    assert day.main(part1=True, use_example=False) == 166630675, "Test: True, False"
    assert day.main(part1=False, use_example=True) == 48, "Test: False, True"
    assert day.main(part1=False, use_example=False) == 93465710, "Test: False, False"


def test_day4():
    day = day4
    assert day.main(part1=True, use_example=True) == 18, "Test: True, True"
    assert day.main(part1=True, use_example=False) == 2507, "Test: True, False"
    assert day.main(part1=False, use_example=True) == 9, "Test: False, True"
    assert day.main(part1=False, use_example=False) == 1969, "Test: False, False"


def test_day5():
    day = day5
    assert day.main(part1=True, use_example=True) == 143, "Test: True, True"
    assert day.main(part1=True, use_example=False) == 5064, "Test: True, False"
    assert day.main(part1=False, use_example=True) == 123, "Test: False, True"
    assert day.main(part1=False, use_example=False) == 5152, "Test: False, False"


def test_day6():
    day = day6
    assert day.main(part1=True, use_example=True) == 41, "Test: True, True"
    assert day.main(part1=True, use_example=False) == 5080, "Test: True, False"
    assert day.main(part1=False, use_example=True) == 6, "Test: False, True"
    assert day.main(part1=False, use_example=False) == 1919, "Test: False, False"


def test_day7():
    day = day7
    assert day.main(part1=True, use_example=True) == 3749, "Test: True, True"
    assert day.main(part1=True, use_example=False) == 1545311493300, "Test: True, False"
    assert day.main(part1=False, use_example=True) == 11387, "Test: False, True"
    assert (
        day.main(part1=False, use_example=False) == 169122112716571
    ), "Test: False, False"


def test_day8():
    day = day8
    assert day.main(part1=True, use_example=True) == 14, "Test: True, True"
    assert day.main(part1=True, use_example=False) == 289, "Test: True, False"
    assert day.main(part1=False, use_example=True) == 34, "Test: False, True"
    assert day.main(part1=False, use_example=False) == 1030, "Test: False, False"


def test_day9():
    day = day9
    assert day.main(part1=True, use_example=True) == 1928, "Test: True, True"
    assert day.main(part1=True, use_example=False) == 6378826667552, "Test: True, False"
    assert day.main(part1=False, use_example=True) == 2858, "Test: False, True"
    assert (
        day.main(part1=False, use_example=False) == 6413328569890
    ), "Test: False, False"


if __name__ == "__main__":
    pytest.main()

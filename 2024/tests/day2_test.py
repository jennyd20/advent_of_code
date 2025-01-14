from operator import is_
import pytest

import day2


def test_no_dups():
    assert not day2.is_safe([1, 1, 2, 3])
    assert not day2.is_safe([99, 100, 102, 104, 105, 105])


def test_strictly_gradual_increase():
    assert day2.is_safe([1, 2, 3, 4, 5])
    assert day2.is_safe([99, 100, 102, 104, 105])


def test_strictly_extreme_increase():
    assert not day2.is_safe([1, 5, 6, 8, 10])
    assert not day2.is_safe([1, 2, 6, 8, 10])
    assert not day2.is_safe([1, 2, 3, 8, 10])
    assert not day2.is_safe([1, 2, 3, 4, 10])
    assert not day2.is_safe([99, 105, 10110, 20000])


def test_strictly_gradual_decrease():
    assert day2.is_safe([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    assert day2.is_safe([1000, 999, 997, 995])


def test_strictly_extreme_decrease():
    assert not day2.is_safe([15, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    assert not day2.is_safe([15, 14, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    assert not day2.is_safe([15, 14, 13, 7, 6, 5, 4, 3, 2, 1, 0])
    assert not day2.is_safe([15, 14, 13, 12, 6, 5, 4, 3, 2, 1, 0])
    assert not day2.is_safe([15, 14, 13, 12, 11, 5])
    assert not day2.is_safe([20000, 10110, 105, 99])


def test_change_inc_dec():
    assert not day2.is_safe([1, 3, 5, 7, 9, 8])
    assert not day2.is_safe([1, 3, 5, 7, 6, 8])
    assert not day2.is_safe([1, 3, 5, 4, 6, 8])
    assert not day2.is_safe([1, 3, 2, 4, 6, 8])
    assert not day2.is_safe([1, 0, 2, 4, 6, 8])
    assert not day2.is_safe([1, 0, 4, 2, 9, 8])


def test_change_dec_inc():
    assert not day2.is_safe([9, 6, 5, 7])
    assert not day2.is_safe([9, 6, 7, 5])
    assert not day2.is_safe([9, 10, 7, 5])
    assert not day2.is_safe([9, 10, 7, 8])


### With a margin for error with the dampener
def test_dups_with_dampener():
    assert day2.is_safe([1, 1, 2, 3], 1)
    assert day2.is_safe([99, 100, 102, 104, 105, 105], 1)
    assert not day2.is_safe([99, 100, 102, 102, 105, 105], 1)
    assert not day2.is_safe([99, 99, 102, 102, 105, 106], 1)
    assert not day2.is_safe([1, 2, 2, 2, 2, 3], 1)


def test_strictly_extreme_increase_with_dampener():
    assert day2.is_safe([1, 5, 6, 8, 10], 1)
    assert not day2.is_safe([1, 5, 6, 8, 15], 1)
    assert not day2.is_safe([1, 2, 6, 8, 10], 1)
    assert not day2.is_safe([1, 2, 6, 10, 15], 1)


def test_strictly_extreme_decrease_with_dampener():
    assert day2.is_safe([15, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], 1)
    assert not day2.is_safe([15, 14, 5, 4, 0], 1)
    assert not day2.is_safe([15, 14, 13, 7, 6, 5, 4, 3, 2, 1, 0], 1)
    assert not day2.is_safe([15, 14, 13, 12, 6, 5, 1, 0], 1)
    assert not day2.is_safe([20000, 10000, 1500, 99], 1)


def test_change_inc_dec_with_dampener():
    assert day2.is_safe([1, 3, 5, 7, 9, 8], 1)
    assert day2.is_safe([1, 3, 5, 7, 6, 8], 1)
    assert day2.is_safe([1, 3, 5, 4, 6, 8], 1)
    assert day2.is_safe([1, 3, 2, 4, 6, 8], 1)
    assert day2.is_safe([1, 0, 2, 4, 6, 8], 1)
    assert not day2.is_safe([1, 0, 4, 2, 9, 8], 1)


def test_change_dec_inc_with_dampener():
    assert day2.is_safe([9, 6, 5, 7], 1)
    assert day2.is_safe([9, 6, 7, 5], 1)
    assert day2.is_safe([9, 10, 7, 5], 1)
    assert not day2.is_safe([9, 10, 7, 8], 1)


def test_others_with_dampener():
    assert day2.is_safe([3, 3, 4, 6], 1)
    assert not day2.is_safe([3, 3, 7, 8], 1)
    assert not day2.is_safe([2, 3, 7, 7, 8], 1)
    assert day2.is_safe([2, 3, 4, 4, 5], 1)
    assert not day2.is_safe([2, 3, 5, 5, 4, 6], 1)
    assert not day2.is_safe([1, 4, 2, 3, 3], 1)
    assert day2.is_safe([5, 3, 3, 2, 1], 1)
    assert not day2.is_safe([1, 2, 6, 3, 7], 1)
    assert day2.is_safe([1, 2, 6, 3, 4], 1)
    assert not day2.is_safe([2, 2, 2, 3, 4], 1)
    assert not day2.is_safe([1, 2, 2, 2, 3, 4], 1)
    assert not day2.is_safe([10, 5, 8, 7, 2, 1], 1)
    assert day2.is_safe([10, 5, 8, 7, 6], 1)


def test_part1_failures_with_dampener():
    assert not day2.is_safe([52, 52, 49, 50, 49], 1)
    assert day2.is_safe([51, 50, 47, 45, 42, 41, 34], 1)
    assert not day2.is_safe([35, 40, 41, 38, 40, 42, 49], 1)
    assert day2.is_safe([32, 35, 33, 34, 35, 38], 1)
    assert day2.is_safe([70, 71, 73, 74, 75, 78, 79, 83], 1)
    assert not day2.is_safe([1, 7, 8, 9, 15, 21], 1)
    assert not day2.is_safe([10, 10, 11, 12, 13, 17], 1)
    assert not day2.is_safe([61, 60, 65, 66, 69, 73], 1)
    assert not day2.is_safe([51, 47, 44, 40, 37, 36, 31], 1)
    assert not day2.is_safe([31, 33, 36, 33, 34, 38], 1)
    assert not day2.is_safe([51, 48, 49, 51, 58, 59, 57], 1)
    assert not day2.is_safe([85, 78, 71, 70, 68], 1)
    assert not day2.is_safe([76, 75, 78, 81, 81, 82, 82], 1)
    assert not day2.is_safe([46, 50, 52, 54, 53, 54, 54], 1)
    assert day2.is_safe([59, 56, 53, 50, 47, 47, 44, 41], 1)
    assert not day2.is_safe([85, 81, 83, 82, 79, 77, 75, 75], 1)
    assert not day2.is_safe([92, 89, 86, 82, 81, 84], 1)


if __name__ == "__main__":
    pytest.main()

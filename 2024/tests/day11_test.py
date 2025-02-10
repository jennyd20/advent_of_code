import pytest

import day11


def test_apply_rules():
    assert day11.apply_rules(0) == [1]
    assert day11.apply_rules(1) == [2024]
    assert day11.apply_rules(10) == [1, 0]
    assert day11.apply_rules(99) == [9, 9]
    assert day11.apply_rules(999) == [2021976]
    assert day11.apply_rules(125) == [253000]
    assert day11.apply_rules(253000) == [253, 0]
    assert day11.apply_rules(7) == [14168]
    assert day11.apply_rules(28676032) == [2867, 6032]
    assert day11.apply_rules(2024) == [20, 24]


def test_calculate_count():
    assert day11.calculate_stone_count(0, 1, {}) == 1
    assert day11.calculate_stone_count(1, 1, {}) == 1
    assert day11.calculate_stone_count(17, 4, {}) == 6
    assert day11.calculate_stone_count(0, 1, {}) == 1
    assert day11.calculate_stone_count(0, 2, {}) == 1
    assert day11.calculate_stone_count(0, 3, {}) == 2
    assert day11.calculate_stone_count(0, 4, {}) == 4
    assert day11.calculate_stone_count(0, 5, {}) == 4
    assert day11.calculate_stone_count(0, 6, {}) == 7
    assert day11.calculate_stone_count(1, 1, {}) == 1
    assert day11.calculate_stone_count(10, 1, {}) == 2
    assert day11.calculate_stone_count(99, 1, {}) == 2
    assert day11.calculate_stone_count(999, 1, {}) == 1

def test_process_input():
    assert day11.process_input("0", 1) == 1
    assert day11.process_input("0", 2) == 1
    assert day11.process_input("0", 3) == 2
    assert day11.process_input("0", 4) == 4
    assert day11.process_input("0", 5) == 4
    assert day11.process_input("0", 6) == 7
    assert day11.process_input("1", 1) == 1
    assert day11.process_input("10", 1) == 2
    assert day11.process_input("99", 1) == 2
    assert day11.process_input("999", 1) == 1
    assert day11.process_input("0 1 10 99 999", 0) == 5
    assert day11.process_input("0 1 10 99 999", 1) == 7
    assert day11.process_input("0 1 10 99 999", 2) == 8
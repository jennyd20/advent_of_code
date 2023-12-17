import pytest

import day5

def test_text_to_almanac_map():
    result = day5.text_to_almanac_map("ignoreme\n1 2 3\n4 5 6")
    assert result == [(1, 2, 3), (4, 5, 6)]



if __name__ == "__main__":
    pytest.main()
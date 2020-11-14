import pytest
import roller


def test_roll_d10():
    test_roller = roller.Roller(10)
    result = test_roller.roll()
    assert len(result) == 1
    assert 1 <= result[0] <= 10


def test_roll_10d10():
    test_roller = roller.Roller(10, 10)
    result = test_roller.roll()
    assert len(result) == 10
    for r in result:
        assert 1 <= r <= 10


def test_roll_10d10_explode_10():
    test_roller = roller.Roller(10, 10, 10)
    result = test_roller.roll()
    assert len(result) == 10
    for r in result:  # if we explode on 10s, no results should actually be 10
        assert r != 10


def test_roll_10d10_reroll_8():
    test_roller = roller.Roller(10, 10, None, 8)
    result = test_roller.roll()
    assert len(result) == 10
    for r in result:  # if we explode on 10s, no results should actually be 10
        if isinstance(r, int):
            assert 1 <= r <= 7  # no single entries should be greater than 7
        else:  # should be a list
            assert 8 <= r[0] <= 10
            assert sum(i > 8 for i in r) < len(
                r)  # number of potential rerolls should be less than the length of result list

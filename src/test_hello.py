"""tests hello.py module"""
import hello


def test_add():
    """tests add method in hello.py"""
    # test basic functionality
    assert hello.add(1, 1) == 2
    # try a border case
    assert hello.add(-1, -1) == -2

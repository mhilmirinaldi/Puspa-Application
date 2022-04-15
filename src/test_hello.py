def test_add():
    import hello
    # test basic functionality
    assert hello.add(1, 1) == 2
    # try a border case
    assert hello.add(-1, -1) == -2

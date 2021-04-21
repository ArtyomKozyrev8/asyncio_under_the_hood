def gen_func():
    """just to show generators behavior"""
    print("A")
    yield "A"
    print("B")
    yield "B"
    print("C")
    yield "C"


if __name__ == '__main__':
    c = gen_func()
    next(c)
    next(c)
    next(c)
    next(c)  # StopIteration error here

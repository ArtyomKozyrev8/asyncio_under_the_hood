def get_fib_num(n: int) -> int:
    """just some heavy cpu bound operation when n is quite a big number"""
    if n <= 1:
        return 1
    return get_fib_num(n-1) + get_fib_num(n-2)

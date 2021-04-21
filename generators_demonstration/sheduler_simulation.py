from collections import deque
import time


def some_generator(n):
    """just some easy generator"""
    while n:
        time.sleep(1)
        print(n)
        yield n
        n -= 1


def loop_scheduler(_q: deque):
    """some kind of loop scheduler which switch between tasks"""
    while _q:
        try:
            gen = _q.pop()
            next(gen)
            _q.appendleft(gen)
        except StopIteration:
            pass


if __name__ == '__main__':
    # deque is used to simulate loop
    q = deque([some_generator(20), some_generator(10)])
    loop_scheduler(q)

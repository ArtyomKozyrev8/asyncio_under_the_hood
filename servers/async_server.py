"""
The code is made based on David Beazley explanation https://www.youtube.com/watch?v=MCs5OvhV9S4
which was demonstrated on PyCon 2015

The solution looks quite similar to SelectSelector in https://github.com/python/cpython/blob/3.9/Lib/selectors.py
"""

import socket
import select
from fibonacci_num.fib_num import get_fib_num
from collections import deque
from concurrent.futures import ProcessPoolExecutor, Future

IP = "localhost"
PORT = 1234

send_sockettasks = {}
recv_sockettasks = {}
calc_tasks = {}

tasks = deque()  # storage for generator functions

r_s, w_s = socket.socketpair()  # is used to notify current process that child process has done work


def calc_task_done_callback(fut: Future):
    """
    Is used to notify current process that child process mad calculations
    It is used by sending b"done" to r_s (r_s is also inside cur process)
    It is not generator function since we need results immediately
    as soon as they are available, like in our client script
    """
    t = calc_tasks.pop(fut)
    tasks.append(t)  # further actions can be done with generator function
    w_s.send(b"done")  # just notify


def monitor_calc_tasks():
    """
    we need somehow receive notification that calc fut was done
    The function is responsible for the operation.
    It listens for messages from calc_task_done_callback.
    And select.select listens for the messages r_s receives from
    calc_task_done_callback
    """
    while True:
        yield "recv", r_s
        r_s.recv(1024)


def scheduler():
    """
    The same type of function as in generators_demonstration/sheduler_simulation.py
    It monitors sockets and generator functions which are stored in tasks deque
    """
    while any([tasks, send_sockettasks, recv_sockettasks, calc_tasks]):
        # if we have not generators in tasks we can spend time on listening
        # for traffic in sockets in order to get new generators and put them in tasks
        while not tasks:
            r, w, _ = select.select(recv_sockettasks, send_sockettasks, [])
            for i in r:
                task = recv_sockettasks.pop(i)
                tasks.append(task)
            for i in w:
                task = send_sockettasks.pop(i)
                tasks.append(task)
        # if we have some generator functions in tasks we can work with them
        # and make them reach a new stage and pause
        while tasks:
            t = tasks.popleft()
            try:
                why, what = next(t)
                if why == "recv":
                    recv_sockettasks[what] = t
                elif why == "send":
                    send_sockettasks[what] = t
                elif why == "calc_task":
                    calc_tasks[what] = t
                    # we add callback because CPU tasks are run in another processes
                    # and we can not monitor them with select.select
                    what.add_done_callback(calc_task_done_callback)
                else:
                    raise RuntimeError("Smth gone wrong")
            except StopIteration:
                print(f"{t} finished")


def handle_connection(conn: socket.socket, pool: ProcessPoolExecutor):
    """Handles connection from client process"""
    while True:
        yield "recv", conn  # pause generator in the place
        # will be resumed by selector
        data = conn.recv(1024)
        n = int(data.decode("utf8"))
        fut = pool.submit(get_fib_num, n)
        yield "calc_task", fut
        res = fut.result()
        yield "send", conn
        conn.send(str(res).encode("utf8"))


def server_run(pool: ProcessPoolExecutor):
    """Listens for incoming connections from clients"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT, ))
        s.listen(1)
        while True:
            yield "recv", s
            conn, addr = s.accept()
            tasks.append(handle_connection(conn=conn, pool=pool))


if __name__ == '__main__':
    with ProcessPoolExecutor() as p:
        tasks.extend(
            [
                server_run(p),
                monitor_calc_tasks()
            ]
        )
        scheduler()

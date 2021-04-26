import socket
import select
from fibonacci_num.fib_num import get_fib_num
from collections import deque

IP = "localhost"
PORT = 1234

send_socket_tasks = {}
recv_socket_tasks = {}
tasks = deque()


def scheduler(_tasks):
    while any([_tasks, send_socket_tasks, recv_socket_tasks]):
        while not _tasks:
            r, w, _ = select.select(recv_socket_tasks, send_socket_tasks, [])
            for i in r:
                task = recv_socket_tasks.pop(i)
                _tasks.append(task)
            for i in w:
                task = send_socket_tasks.pop(i)
                _tasks.append(task)
        while _tasks:
            t = _tasks.popleft()
            try:
                why, what = next(t)
                if why == "recv":
                    recv_socket_tasks[what] = t
                elif why == "send":
                    send_socket_tasks[what] = t
                else:
                    raise RuntimeError("Smth gone wrong")
            except StopIteration:
                print(f"{t} finished")


def handle_connection(conn: socket.socket):
    while True:
        yield "recv", conn
        data = conn.recv(1024)
        n = int(data.decode("utf8"))
        res = get_fib_num(n)
        yield "send", conn
        conn.send(str(res).encode("utf8"))


def server_run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT, ))
        s.listen(5)
        while True:
            yield "recv", s
            conn, addr = s.accept()
            tasks.append(handle_connection(conn=conn))


if __name__ == '__main__':
    tasks.append(server_run())
    scheduler(tasks)

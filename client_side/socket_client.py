import socket
import sys
import threading as th
import time

IP = "127.0.0.1"
PORT = 7474


class ReqCounter:
    """Counter to calculate number of request per second"""
    def __init__(self):
        self.n = 0
        self.lock = th.Lock()

    def increment(self):
        with self.lock:
            self.n += 1

    def _clear(self):
        with self.lock:
            self.n = 0

    def show_req_num(self):
        print(f"RPS: {self.n}")
        self._clear()


def send_message(conn: socket.socket, counter: ReqCounter, n: int) -> None:
    """Just send number to server and increases counter"""
    conn.send(str(n).encode('utf8'))
    d = conn.recv(1024)
    counter.increment()


def show_results_th(c: ReqCounter):
    """Thread target function to display RPS"""
    while True:
        time.sleep(1)
        c.show_req_num()


if __name__ == '__main__':
    num = int(sys.argv[1])  # should be provided and be integer number
    _counter = ReqCounter()

    th.Thread(target=show_results_th, args=(_counter, ), daemon=True).start()

    # create connection with server
    with socket.create_connection((IP, PORT,)) as s:
        # just send requests infinitely
        while True:
            send_message(s, _counter, num)

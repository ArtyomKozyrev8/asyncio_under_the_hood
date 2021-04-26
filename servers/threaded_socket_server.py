import socket
from fibonacci_num.fib_num import get_fib_num
from threading import Thread
from concurrent.futures import ProcessPoolExecutor

IP = "127.0.0.1"
PORT = 7474


def on_accept(_conn: socket.socket, pool: ProcessPoolExecutor) -> None:
    """infinitely get data and return response after calculations"""
    while True:
        data = _conn.recv(1024)
        n = int(data.decode('utf8'))
        fut = pool.submit(get_fib_num, n)
        f_num = fut.result()
        _conn.send(str(f_num).encode('utf8'))


def serve_forever(ip: str, port: int) -> None:
    with ProcessPoolExecutor(4) as p:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, port, ))
            print(f"Running on {ip}:{port}")
            s.listen(5)
            while True:
                conn, addr = s.accept()  # get connection
                print(f"Established connection with {addr[0]}:{addr[1]}")
                # move all response logic to another thread and keep waiting for new connections
                Thread(target=on_accept,  args=(conn, p, )).start()


if __name__ == '__main__':
    serve_forever(IP, PORT)

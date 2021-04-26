import socket

IP = "localhost"
PORT = 1234

with socket.create_connection((IP, PORT, )) as s:
    while True:
        for i in range(25, 39):
            s.send(str(i).encode("utf8"))
            data = s.recv(1024)
            data = f"{i}: {data.decode('utf8')}"
            print(data)

#python client_side/client_for_async_server.py
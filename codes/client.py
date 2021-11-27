import socket
from query import Query

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 42069))

    s.send(Query(3).encode())

    # data = s.recv(4096)
    _ = input()
    s.close()

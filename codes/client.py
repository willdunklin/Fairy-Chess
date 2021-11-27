import socket
import json

class Query:
    def __init__(self, move, board) -> None:
        self.q = json.dumps({'query': move, 'exwit': 0, 'board': board}).encode('utf-8')

    def encode(self) -> bytes:
        return self.q

board = {}
queue = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 42069))
    s.settimeout(5)

    queue.append(Query(3, board).encode())

    for q in queue:
        s.send(q)

    queue = []

    data = s.recv(4096)

    s.close()

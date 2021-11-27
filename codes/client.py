import socket
import json

from codes.server_game import SGame

class Query:
    def __init__(self, move, board) -> None:
        self.q = json.dumps({'query': move, 'exwit': 0, 'board': board}).encode('utf-8')

    def encode(self) -> bytes:
        return self.q

queue = []
local_game = SGame()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 42069))

    s.settimeout(1.5)
    for _ in range(10):

        # send messages in queue
        # TODO: might not be necessary to maintain queue
        queue.append(Query(3, local_game.board).encode())
        for q in queue:
            s.send(q)
        queue = []

        # receive message from server
        try:
            data = s.recv(4096)
        except socket.timeout:
            continue

        if not data:
            continue

        try:
            msg: dict = json.loads(data.decode('utf-8'))
                
            if msg.get('invalid') != None:
                # the proposed move was invalid
                pass

            # update local board record 
            if msg.get('board') != None:
                local_game.set_board(msg['board'])

            print(msg)

        except Exception as e:
            s.close()
            print(e)
            raise(e)

    s.close()

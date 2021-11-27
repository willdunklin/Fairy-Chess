import socket
import json 
import threading
from server_game import SGame

connections = {}
game = SGame()

def receive(conn: socket.socket):
    global game

    loop = True
    # timeout for recv
    conn.settimeout(1.5)
    local_board = ''

    while loop:
        # try within timeout
        try:
            data = conn.recv(4096)
        except socket.timeout:
            continue

        # if there is a discrepency between the clients board and the game's resend
        # exepects client to respond
        if game.board_string() != local_board:
            conn.send(json.dumps({'board': game.board_string()}))

        if not data:
            continue

        try:
            msg: dict = json.loads(data.decode('utf-8'))
            
            if msg.get('exit') != None:
                print('exiting connection')
                loop = False
            
            if msg.get('query') != None:
                # Game.check_move()
                # game plays move -> returns board or None for invalid move
                result = game.play(msg['query'])
                if result == False:
                    conn.send(json.dumps({'invalid': 0}))
                print(msg['query'])
            
            # update local board record 
            if msg.get('board') != None:
                local_board = msg['board']

            print(msg)

        except Exception as e:
            conn.close()
            print(e)
            raise(e)

    conn.close()


def accept():
    global connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 42069))
        s.listen(5)

        for _ in range(3):
            conn, addr = s.accept()
            print(addr)

            t = threading.Thread(target=receive, args=(conn,))
            t.start()

            if connections.get(addr) != None:
                print('!!!')
    
            connections[addr] = (t, conn)

if __name__ == '__main__':
    accept()
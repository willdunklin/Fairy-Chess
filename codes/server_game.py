import json

class SGame:
    def __init__(self) -> None:
        self.board = {}

    def board_string(self) -> str:
        return str(self.board)

    def set_board(self, board_string: str) -> dict:
        self.board = json.loads(board_string)
        return self.board

    def play(self, move) -> bool:
        '''
        play a move on the board
        returns whether move is legal
        '''
        return False
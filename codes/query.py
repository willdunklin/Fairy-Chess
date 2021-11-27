import json

class Query:
    def __init__(self, move) -> None:
        self.q = json.dumps({'query': move, 'ewxit': 0}).encode('utf-8')

    def encode(self) -> bytes:
        return self.q
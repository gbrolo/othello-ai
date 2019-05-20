import numpy as np
INITIAL_BOARD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
DIRECTIONS = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

class Board():

    def __init__(self):
        self.directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]
        self.board = []

    def numpyfy_board(self, board):    
        return np.reshape(np.array(board), (8, 8))

    def get_squares(self, color):
        squares = []

        for y in range(8):
            for x in range(8):
                if self.board[x][y] == color:
                    squares.append((x,y))
        
        return squares

    def get_moves_square(self, square):
        (x,y) = square
        color = self.board[x][y]

        if color == 0:
            return None

        possible_moves = []
        for direction in self.directions:
            move = self.search_move(square, direction)
            if move:
                possible_moves.append(move)

        return possible_moves

    def search_move(self, origin, direction):
        x,y = origin
        color = self.board[x][y]
        flips = []

        for x,y in self.augment_move(origin, direction):
            if self.board[x][y] == 0 and flips:
                return (x,y)
            elif (self.board[x][y] == color or (self.board[x][y] == 0 and not flips)):
                return None
            elif self.board[x][y] == self.get_contrary_color(color):
                flips.append((x,y))

    def get_contrary_color(self, color):
        return 1 if color == 2 else 2

    @staticmethod
    def augment_move(move, direction):
        move = map(sum, zip(move, direction))

        while all(map(lambda x: 0 <= x < 8, move)):
            yield move
            move = map(sum, zip(move, direction))

    def get_legal_moves(self, color):
        moves = set()

        for square in self.get_squares(color):
            updated_moves = self.get_moves_square(square)
            moves.update(updated_moves)

        return list(moves)

    def convert_single_move(self, move):
        (x,y) = move
        return str(x + 1) + chr(ord('a') + y)

    def convert_moves(self, moves):
        converted_moves = []

        for move in moves:
            converted_moves.append(self.convert_single_move(move))
        
        return converted_moves

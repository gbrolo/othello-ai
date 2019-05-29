import numpy as np

class Board():

    def __init__(self):
        self.directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]
        self.board = []

    def numpyfy_board(self, board):    
        return np.reshape(np.array(board), (8, 8))

    def get_tiles(self, color):
        tiles = []

        for y in range(8):
            for x in range(8):
                if self.board[x][y] == color:
                    tiles.append((x,y))
        
        return tiles

    def get_moves_tile(self, tile):
        (x,y) = tile
        color = self.board[x][y]

        if color == 0:
            return None

        possible_moves = []
        for direction in self.directions:
            move = self.search_move(tile, direction)
            if move:
                possible_moves.append(move)

        return possible_moves

    def run_move(self, move, color):
        flips = (
            flip for direction in self.directions for flip in self.apply_flips(move, direction, color)
        )

        for x,y in flips:
            self.board[x][y] = color

    def search_move(self, tile, direction):
        x,y = tile
        color = self.board[x][y]
        flips = []

        for x,y in self.augment_move(tile, direction):
            if self.board[x][y] == 0 and flips:
                return (x,y)
            elif (self.board[x][y] == color or (self.board[x][y] == 0 and not flips)):
                return None
            elif self.board[x][y] == self.get_contrary_color(color):
                flips.append((x,y))

    def apply_flips(self, tile, direction, color):
        flips = [tile]

        for x,y in self.augment_move(tile, direction):
            if self.board[x][y] == self.get_contrary_color(color):
                flips.append((x,y))
            elif self.board[x][y] == 0:
                break
            elif len(flips) > 1 and self.board[x][y] == color:
                return flips

        return []

    def get_contrary_color(self, color):
        return 1 if color == 2 else 2

    def count_tiles(self, color):               
        return np.reshape(self.board.tolist(), (1, 64))[0].tolist().count(color)

    @staticmethod
    def augment_move(move, direction):
        move = map(sum, zip(move, direction))
        while all(map(lambda x: 0 <= x <= 7, move)):
            yield move
            move = map(sum, zip(move, direction))

    def get_legal_moves(self, color):
        moves = set()

        for tile in self.get_tiles(color):
            updated_moves = self.get_moves_tile(tile)
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

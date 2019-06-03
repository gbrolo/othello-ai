import numpy as np

class Board():

    def __init__(self):
        # possible directions a new move could take from a tile
        self.directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]
        self.board = []

    # create an 8x8 board as a numpy array
    def numpyfy_board(self, board):    
        return np.reshape(np.array(board), (8, 8))

    # get tiles for specified color
    def get_tiles(self, color):
        tiles = []

        for y in range(8):
            for x in range(8):
                if self.board[x][y] == color:
                    tiles.append((x,y))
        
        return tiles

    # return possible valid moves a player can take from a tile with his color
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

    # apply some move to current board
    def run_move(self, move, color):
        flips = (
            flip for direction in self.directions for flip in self.apply_flips(move, direction, color)
        )

        for x,y in flips:
            self.board[x][y] = color

    # search for valid moves you can take inside current board
    def search_move(self, tile, direction):
        x,y = tile
        color = self.board[x][y]
        # flips are tiles from opponent now converted to your color after some move
        flips = []

        for x,y in self.augment_move(tile, direction):
            if self.board[x][y] == 0 and flips:
                return (x,y)
            elif (self.board[x][y] == color or (self.board[x][y] == 0 and not flips)):
                return None
            elif self.board[x][y] == self.get_contrary_color(color):
                flips.append((x,y))

    # apply flips (change of color in tiles) in board
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

    # return opponent's color
    def get_contrary_color(self, color):
        return 1 if color == 2 else 2

    # count number of tiles in current board for provided color
    def count_tiles(self, color):               
        return np.reshape(self.board.tolist(), (1, 64))[0].tolist().count(color)

    # create generator that yields possible moves to take
    @staticmethod
    def augment_move(move, direction):
        # get move to apply
        move = get_tuple_move(move, direction)  

        # yield move only if position is a valid one inside the board, i.e, has a value between 0 and 7 inclusive             
        while all(map(lambda x: 0 <= x <= 7, move)):
            yield move
            move = get_tuple_move(move, direction)     

    # get all valid moves you can take
    def get_legal_moves(self, color):
        moves = set()

        for tile in self.get_tiles(color):
            updated_moves = self.get_moves_tile(tile)
            moves.update(updated_moves)

        return list(moves)

    # convert tuple (x,y) into othello board tile i.e 1A, 2B, etc.
    def convert_single_move(self, move):
        (x,y) = move
        return str(x + 1) + chr(ord('a') + y)

    # convert all tuples (x,y) into othello board tiles i.e 1A, 2B, etc.
    def convert_moves(self, moves):
        converted_moves = []

        for move in moves:
            converted_moves.append(self.convert_single_move(move))
        
        return converted_moves

# aids in creating generator for possible moves, by applying a direction to a current tile and returning that move
def get_tuple_move(move, direction):
        # create tuple with current tile position and valid direction
        tuples = zip(move, direction)        
        # generate move based on applying valid direction into current tile position
        move = map(sum, tuples) 
        return move
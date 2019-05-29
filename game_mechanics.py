from board_utils import *
from ai_engine import *
from copy import deepcopy
import random
import timeit

def get_possibilities(board, player_turn_id):
    b = Board()
    b.board = b.numpyfy_board(board)
    print(b.board)
    legal_moves = b.get_legal_moves(player_turn_id)    
    moves = b.convert_moves(legal_moves)       
    return moves

def show_board(board):
    b = Board()
    b.board = b.numpyfy_board(board)
    print(b.board)

    print('Captured tiles [1]: ' + str(b.count_tiles(1)) + ', Captured tiles [2]: ' + str(b.count_tiles(2)))    

def select_first_possibility(moves):
    move = random.choice(moves)    
    converted_move = convert_move_to_tile(move)
    return converted_move

def convert_move_to_tile(move):
    letters = 'abcdefgh'
    return ((int(move[0]) - 1) * 8) + letters.find(move[1])

def make_a_move(board, player_turn_id):
    start_time = timeit.default_timer()
    b = Board()
    b.board = b.numpyfy_board(board)
    print(b.board)

    engine = AI()
    return convert_move_to_tile(b.convert_moves([ai_move(engine, b, player_turn_id, start_time)])[0])    


def ai_move(engine, board, color, time):
    legal_moves = board.get_legal_moves(color)

    return engine.minimax_alpha_beta(
        deepcopy(board),
        color,
        time
    )

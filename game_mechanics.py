from board_utils import *
from ai_engine import *
from copy import deepcopy
import random
import timeit

INITIAL_BOARD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def get_possibilities(board, player_turn_id):
    b = Board()
    b.board = b.numpyfy_board(board)
    print(b.board)
    legal_moves = b.get_legal_moves(player_turn_id)
    print(legal_moves)
    moves = b.convert_moves(legal_moves)   
    print(moves) 
    return moves

def show_board(board):
    b = Board()
    b.board = b.numpyfy_board(board)
    print(b.board)

    print('Player 1 captured tiles: ', b.count_tiles(1))
    print('Player 2 captured tiles: ', b.count_tiles(2))

def select_first_possibility(moves):
    move = random.choice(moves)
    print(move)
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

    move = ai_move(engine, b, player_turn_id, 1, start_time)
    moves = [move]
    moves = b.convert_moves(moves)
    move = moves[0]
    converted_move = convert_move_to_tile(move)
    return converted_move    


def ai_move(engine, board, color, movement_number, time):
    legal_moves = board.get_legal_moves(color)

    if not legal_moves:
        return None
    elif len(legal_moves) == 1:
        return legal_moves[0]
    else:
        move = engine.retrieve_move(
            deepcopy(board),
            color,
            movement_number,
            time
        )

        return move

# first = select_first_possibility(get_possibilities(INITIAL_BOARD, 1))
# print(first)
# move = make_a_move(INITIAL_BOARD, 1)
# print(move)

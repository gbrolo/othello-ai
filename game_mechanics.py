from board_utils import *
import random

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

def select_first_possibility(moves):
    move = random.choice(moves)
    print(move)
    converted_move = convert_move_to_tile(move)
    return converted_move

def convert_move_to_tile(move):
    letters = 'abcdefgh'
    return ((int(move[0]) - 1) * 8) + letters.find(move[1])
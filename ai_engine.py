import random
from board_utils import *
from copy import deepcopy

class AI():
    def __init__(self):
        self.inf = float('inf')
        self.b_list = [0, 0, 0]
        self.weights = [
             4, -3,  2,  2,  2,  2, -3,  4,
            -3, -4, -1, -1, -1, -1, -4, -3,
             2, -1,  1,  0,  0,  1, -1,  2,
             2, -1,  0,  1,  1,  0, -1,  2,
             2, -1,  0,  1,  1,  0, -1,  2,
             2, -1,  1,  0,  0,  1, -1,  2,
            -3, -4, -1, -1, -1, -1, -4, -3,
             4, -3,  2,  2,  2,  2, -3,  4
        ]

    def retrieve_move(self, board, color, movement_number=None, remaining_time=None):
        return self.minimax_alpha_beta(board, color, movement_number, remaining_time, 4)

    def heuristic(self, board, color):
        return 2 * self.corner_weight(color, board) + 2 * self.get_cost(board, color)

    def corner_weight(self, color, board):
        total = 0
        for i in range(0, 64):
            if board.board[i / 8][i % 8] == color:
                total += self.weights[i]
            if board.board[i / 8][i % 8] == board.get_contrary_color(color):
                total -= self.weights[i]
            
        return total

    def get_cost(self, board, color):
        current_color = board.count_tiles(color)
        contrary_color = board.count_tiles(
            board.get_contrary_color(color)
        )

        return current_color - contrary_color

    def greedy_choice(self, board, color, move):
        new_board = deepcopy(board)
        new_board.run_move(move, color)

        current_color = new_board.count_tiles(color)
        contrary_color = new_board.count_tiles(
            board.get_contrary_color(color)
        )

        return current_color - contrary_color

    def max_score(self, board, contrary_color, movement_number, depth, alpha, beta):
        if depth == 0:
            return self.heuristic(board, contrary_color)

        best_score = -self.inf

        for m in board.get_legal_moves(contrary_color):
            new_board = deepcopy(board)
            new_board.run_move(m, contrary_color)

            score = self.min_score(
                new_board,
                board.get_contrary_color(contrary_color),
                movement_number,
                depth - 1,
                alpha,
                beta
            )

            if score > best_score:
                best_score = score
                
            if best_score >= beta:
                return best_score

            alpha = max(alpha, best_score)

        return best_score

    def min_score(self, board, contrary_color, movement_number, depth, alpha, beta):
        if depth == 0:
            return self.heuristic(board, contrary_color)

        best_score = self.inf

        for m in board.get_legal_moves(contrary_color):
            new_board = deepcopy(board)
            new_board.run_move(m, contrary_color)

            score = self.max_score(
                new_board, 
                board.get_contrary_color(contrary_color),
                movement_number,
                depth - 1,
                alpha,
                beta
            )

            if best_score > score:
                best_score = score
            if best_score <= alpha:
                return best_score

            beta = min(beta, best_score)

        return best_score


    def minimax_alpha_beta(self, board, color, movement_number, remaining_time, depth=4):
        moves = board.get_legal_moves(color)

        move = moves[0]
        best_score = -self.inf

        if remaining_time < 5:
            return(max(moves, key=lambda x: self.greedy_choice(board, color, x)))
        
        for m in moves:
            new_board = deepcopy(board)
            new_board.run_move(m, color)
            self.b_list[0] += 1

            score = self.min_score(
                new_board,
                board.get_contrary_color(color),
                movement_number,
                depth - 1,
                -self.inf,
                self.inf
            )

            if score > best_score:
                best_score = score
                move = m

        return move

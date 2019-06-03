import random
from board_utils import *
from copy import deepcopy
import timeit

class AI():
    def __init__(self):
        self.inf = float('inf')        
        # heuristic weights got from paper 'An Analysis of Heuristics in Othello'        
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

    def heuristic(self, board, color):
        if (color == 2):
            return self.corner_weight(color, board) + 8 * self.get_cost(color, board) + 4 * self.corner_ocupancies(color, board)
        elif (color == 1):
            return self.corner_weight(color, board) + 4 * self.get_cost(color, board) + 8 * self.corner_ocupancies(color, board)

    def corner_weight(self, color, board):
        total = 0
        b = np.reshape(board.board.tolist(), (1, 64))[0].tolist()
        for i in range(0, 64):
            total = total + 1 if b[i] == color else total - 1 if b[i] == board.get_contrary_color(color) else total            

        return total    

    def corner_ocupancies(self, color, board):
        contrary_color = board.get_contrary_color(color)
        tiles = 0
        contrary_tiles = 0

        corners = [
            board.board[0][0],
            board.board[0][7],
            board.board[7][0],
            board.board[7][7],
        ]

        for corner in corners:
            if (corner == color):
                tiles += 1
            elif (corner == contrary_color):
                contrary_tiles += 1

        return 25 * (tiles - contrary_tiles)

    def get_cost(self, color, board):
        current_color = board.count_tiles(color)
        contrary_color = board.count_tiles(
            board.get_contrary_color(color)
        )

        return current_color - contrary_color

    def select_greedy_type(self, color, board):
        tiles_vs_opponent = self.get_cost(color, board)
        blank_tiles = board.count_tiles(0)

        if tiles_vs_opponent <= 0 and tiles_vs_opponent <= blank_tiles:
            return True
        else:
            return False

    def greedy_choice(self, board, color, move):
        print('Greedy choice')
        new_board = deepcopy(board)
        new_board.run_move(move, color)

        current_color = new_board.count_tiles(color)
        contrary_color = new_board.count_tiles(
            board.get_contrary_color(color)
        )

        return current_color - contrary_color

    def max_score(self, board, contrary_color, depth, alpha, beta):
        if depth == 0:
            return self.heuristic(board, contrary_color)

        best_score = -self.inf

        for m in board.get_legal_moves(contrary_color):
            new_board = deepcopy(board)
            new_board.run_move(m, contrary_color)

            score = self.min_score(
                new_board,
                board.get_contrary_color(contrary_color),                
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

    def min_score(self, board, contrary_color, depth, alpha, beta):
        if depth == 0:
            return self.heuristic(board, contrary_color)

        best_score = self.inf

        for m in board.get_legal_moves(contrary_color):
            new_board = deepcopy(board)
            new_board.run_move(m, contrary_color)

            score = self.max_score(
                new_board, 
                board.get_contrary_color(contrary_color),                
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


    def minimax_alpha_beta(self, board, color, remaining_time, depth=4):
        moves = board.get_legal_moves(color)

        move = moves[0]
        best_score = -self.inf                
        
        for m in moves:
            current_time = timeit.default_timer()            
            time_diff = current_time - remaining_time            

            if time_diff >= 1.0:
                # greedy_type = random.randint(1,2)
                if (not self.select_greedy_type(color, board)):
                    print('Greedy random')                                    
                    return select_random_possibility(board, color)
                else:
                    return(max(moves, key=lambda x: self.greedy_choice(board, color, x)))        

            new_board = deepcopy(board)
            new_board.run_move(m, color)            

            score = self.min_score(
                new_board,
                board.get_contrary_color(color),                
                depth - 1,
                -self.inf,
                self.inf
            )

            if score > best_score:
                best_score = score
                move = m        

        return move

def select_random_possibility(board, player_turn_id):
    return random.choice(board.get_legal_moves(player_turn_id))

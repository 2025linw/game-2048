from math import inf
from game2048 import Board, N

from random import choice as choose

# Weights for heuristic - Many research papers use these values
A = 4096 # Weight on empty tiles
B = 10 # Weight for the sum of neighboring tile's differences
C = 10 # Sum of the distances to the closest border

# Ratio for Monte Carlo
MC_RATIO = 0.3 # Ratio for 

def heuristic_function(grid):
    E = 0
    D = 0
    P = 0

    # Number of empty tiles
    E = len(list(Board.get_empty_cells(grid)))

    # Sum of neighboring tiles
    for r in range(N):
        for c in range(N):
            if not grid[r][c]: continue

            if c != 0 and grid[r][c-1]: # Left
                D += abs(grid[r][c] - grid[r][c -1])
            if r != 0 and grid[r-1][c]: # Up
                D += abs(grid[r][c] - grid[r-1][c])
            if c != N-1 and grid[r][c+1]: # Right
                D += abs(grid[r][c] - grid[r][c+1])
            if r != N-1 and grid[r+1][c]: # Down
                D += abs(grid[r][c] - grid[r+1][c])

    # Sum of distances to closest border
    for r in range(N):
        for c in range(N):
            if not grid[r][c]: continue

            min_dist = min(r, c, N - 1 - r, N - 1 - c)
            P +=  min_dist * grid[r][c]

    return A * E - B * D - C * P


class RandomAI(Board):
    def __init__(self, verbose=False):
        super()
        self.verbose = verbose

    def make_move(self):
        dir = choose(self.get_moves())
        self.move(dir)

        if self.verbose:
            print("Chose: {}".format(dir))

class GreedyAI(Board):
    def __init__(self, verbose=False):
        super()
        self.verbose = verbose

    def make_move(self):
        dir = ""
        max = -1
        for move in self.get_moves():
            _, score = Board.sim_move(self.grid, move)
            if score > max:
                dir = move
                max = score

        self.move(dir)

        if self.verbose:
            print("Chose: {}".format(dir))

class SimpleMonteCarloAI(Board):
    def __init__(self, depth=3, iteration=100, verbose=False):
        pass

class ExpectimaxAI(Board):
    def __init__(self, board, depth):
        pass

class AveragedDLS(Board):
    def __init__(self, depth=3, iterations=100, verbose=False):
        super()
        self.depth = depth
        self.iterations = iterations
        self.verbose = verbose

    def make_move(self):
        if self.terminal():
            return None

        dir, _ = self.search(self.grid, self.depth - 1)

        self.move(dir)

        if self.verbose:
            print("Chose: {}".format(dir))

    def search(self, grid, depth, h=heuristic_function):
        best_dir = ""
        best_expect_val = -inf

        moves = list(Board.get_valid_moves(grid))
        if not moves:
            return None, -inf
        for move in moves: # Loop through all possible
            sum_expect_val = 0
            for i in range(self.iterations):
                next_grid, _ = Board.sim_full_move(grid, move)

                if depth == 0:
                    sum_expect_val += h(next_grid)
                else:
                    dir, value = self.search(next_grid, depth - 1)
                    if not dir: continue
                    sum_expect_val += value

            avg_expect_val = sum_expect_val / self.iterations

            if avg_expect_val > best_expect_val:
                best_dir = move
                best_expect_val = avg_expect_val

        return best_dir, best_expect_val

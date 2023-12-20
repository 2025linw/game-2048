# Inspiration for Board construction taken from Kuang-che Wu
# https://github.com/kcwu/2048-python

from random import random as rand, choice as choose
from copy import deepcopy

N = 4

possible_moves = ["up", "down", "left", "right"]

class Board(object):
    # Constructor
    def __init__(self):
        self.grid = Board.empty_board()
        self.score = 0
        self.moves = 0

    # Static Methods
    @staticmethod
    def empty_board():
        return [[None] * N for _ in range(N)]

    @staticmethod
    def get_highest_tile(grid):
        max_val = 0
        for r in range(N):
            for c in range(N):
                if grid[r][c] is None:
                    continue

                if grid[r][c] > max_val:
                    max_val = grid[r][c]

        return max_val

    @staticmethod
    def get_empty_cells(grid):
        for r in range(N):
            for c in range(N):
                if grid[r][c] is None:
                    yield r, c

    @staticmethod
    def get_valid_moves(grid):
        for move in possible_moves:
            if Board.sim_move(grid, move)[0] != grid:
                yield move

    @staticmethod
    def sim_rotate_cw(grid):
        out_board = Board.empty_board()

        for r in range(N):
            for c in range(N):
                out_board[c][(N - 1) - r] = grid[r][c]

        return out_board

    @staticmethod
    def sim_rotate_ccw(grid):
        out_board = Board.empty_board()

        for r in range(N):
            for c in range(N):
                out_board[(N - 1) - c][r] = grid[r][c]

        return out_board

    @staticmethod
    def sim_move(grid, direction):
        out_grid = deepcopy(grid)
        score: int = 0

        if direction not in possible_moves:
            return None, 0

        if direction == 'left':
            rot = 0
        elif direction == 'down':
            rot = 1
        elif direction == 'right':
            rot = 2
        elif direction == 'up':
            rot = 3

        for _ in range(rot):
            out_grid = Board.sim_rotate_cw(out_grid)

        for r in range(N):
            row = out_grid[r]

            for oc in range(N):
                for ic in range(oc+1, N):
                    if not row[ic]: # If there is no tile
                        continue

                    if not row[oc]: # Slide
                        row[oc] = row[ic]
                        row[ic] = None
                    elif row[oc] == row[ic]: # Merge
                        row[oc] = row[oc] + row[ic]
                        score += row[oc]

                        row[ic] = None
                        break
                    elif row[oc] != row[ic]:
                        break

        for _ in range(rot):
            out_grid = Board.sim_rotate_ccw(out_grid)

        return out_grid, score

    @staticmethod
    def sim_full_move(grid, direction):
        out_grid = deepcopy(grid)
        score: int = 0

        if direction not in possible_moves:
            return None, 0

        if direction == 'left':
            rot = 0
        elif direction == 'down':
            rot = 1
        elif direction == 'right':
            rot = 2
        elif direction == 'up':
            rot = 3

        for _ in range(rot):
            out_grid = Board.sim_rotate_cw(out_grid)

        for r in range(N):
            row = out_grid[r]

            for oc in range(N):
                for ic in range(oc+1, N):
                    if not row[ic]: # If there is no tile
                        continue

                    if not row[oc]: # Slide
                        row[oc] = row[ic]
                        row[ic] = None
                    elif row[oc] == row[ic]: # Merge
                        row[oc] = row[oc] + row[ic]
                        score += row[oc]

                        row[ic] = None
                        break
                    elif row[oc] != row[ic]:
                        break

        for _ in range(rot):
            out_grid = Board.sim_rotate_ccw(out_grid)

        if grid == out_grid:
            return None, 0

        empty_cells = list(Board.get_empty_cells(out_grid))
        if not empty_cells:
            return out_grid, score
        else:
            if rand() < 0.9:
                v = 2
            else:
                v = 4

            cell_pos = choose(empty_cells)

            out_grid[cell_pos[0]][cell_pos[1]] = v

        return out_grid, score

    # Methods
    ## Utility
    def print(self):
        for r in range(N):
            for c in range(N):
                if c == 0:
                    print("[", end="")

                print("{}".format(self.grid[r][c] if self.grid[r][c] else 0), end="")

                if c == N - 1:
                    print("]", end="\n")
                else:
                    print("|", end="")
        print("Score: {}".format(self.score))
        print("Moves: {}".format(self.moves))

    def terminal(self):
        if not Board.get_empty_cells(self.grid):
            return False

        return not self.get_moves()

    def get_moves(self):
        return list(Board.get_valid_moves(self.grid))

    def get_max_tile(self):
        max_val = 0

        for r in range(N):
            for c in range(N):
                val = self.grid[r][c]
                if not val:
                    continue

                max_val = max(max_val, val)

        return max_val

    ## Game Play Methods
    def start(self):
        self.grid = Board.empty_board()
        self.score = 0
        self.moves = 0
        self.spawnTile()
        self.spawnTile()

    def spawnTile(self):
        empty_cells = list(Board.get_empty_cells(self.grid))
        if not empty_cells:
            return False

        if rand() < 0.9:
            v = 2
        else:
            v = 4

        cell_pos = choose(empty_cells)

        self.grid[cell_pos[0]][cell_pos[1]] = v

        return True

    ## Board Moves
    def rotate_cw(self):
        self.grid = Board.sim_rotate_cw(self.grid)

    def rotate_ccw(self):
        self.grid = Board.sim_rotate_ccw(self.grid)

    def move(self, direction):
        grid, score = Board.sim_move(self.grid, direction)

        if not grid:
            raise Exception("Error occured in move function: Got NoneType")

        moved = self.grid != grid

        self.grid = grid
        self.score += score

        if moved:
            self.moves += 1
            self.spawnTile()

# Inspiration for Board construction taken from Kuang-che Wu
# https://github.com/kcwu/2048-python

from random import random as rand, choice as choose
from copy import deepcopy

BOARD_SIZE = 4

possible_moves = ["up", "down", "left", "right"]

class Board(object):
    # Constructor
    def __init__(self):
        self.grid = Board.empty_board()
        self.score = 0
        self.moves = 0

    # Static Methods
    @staticmethod
    def empty_board() -> list[list[int]]:
        return [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    @staticmethod
    def rotate_cw(grid) -> list[list[int]]:
        out_board = Board.empty_board()

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                out_board[c][(BOARD_SIZE - 1) - r] = grid[r][c]

        return out_board

    @staticmethod
    def rotate_ccw(grid) -> list[list[int]]:
        out_board = Board.empty_board()

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                out_board[(BOARD_SIZE - 1) - c][r] = grid[r][c]

        return out_board

    # Methods
    ## Game Utility Methods
    def print(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if c == 0:
                    print("[", end="")

                print("{}".format(self.grid[r][c] if self.grid[r][c] else 0), end="")

                if c == BOARD_SIZE-1:
                    print("]", end="\n")
                else:
                    print("|", end="")

        print("Score: {}".format(self.score))
        print("Moves: {}".format(self.moves))

    def is_terminal(self) -> bool:
        if not self.get_empty_cells():
            return False

        return not self.get_valid_moves()

    def get_empty_cells(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if not self.grid[r][c]:
                    yield r, c

    def get_valid_moves(self):
        for move in possible_moves:
            if self.sim_move(move)[0] != self.grid:
                yield move

    def spawn_tile(self) -> bool:
        empty_cells = list(self.get_empty_cells())
        if not empty_cells:
            return False

        if rand() < 0.9:
            v = 2
        else:
            v = 4

        cell_row, cell_col = choose(empty_cells)

        self.grid[cell_row][cell_col] = v

        return True

    def start_game(self) -> bool:
        self.grid = Board.empty_board()
        self.score = 0
        self.moves = 0

        self.spawn_tile()
        self.spawn_tile()

    def sim_move(self, direction: str) -> tuple[list[list[int]] | None, int]:
        out_grid = deepcopy(self.grid)
        score = 0

        if direction not in possible_moves:
            return None, 0

        match direction:
            case 'left':
                rot = 0
            case 'down':
                rot = 1
            case 'right':
                rot = 2
            case 'up':
                rot = 3

        for _ in range(rot):
            out_grid = Board.rotate_cw(out_grid)

        for r in range(BOARD_SIZE):
            row = out_grid[r]

            for oc in range(BOARD_SIZE):
                for ic in range(oc+1, BOARD_SIZE):
                    if not row[ic]: # if there is no tile
                        continue

                    if not row[oc]: # slide
                        row[oc] = row[ic]
                        row[ic] = None
                    elif row[oc] == row[ic]: # merge
                        row[oc] = row[oc] + row[ic]
                        score += row[oc]

                        row[ic] = None
                        break
                    elif row[oc] != row[ic]:
                        break

        for _ in range(rot):
            out_grid = Board.rotate_ccw(out_grid)

        return out_grid, score

    ## Game Stats Methods
    def get_max(self) -> int:
        max_val = 0

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if not self.grid[r][c]:
                    continue

                if self.grid[r][c] > max_val:
                    max_val = self.grid[r][c]

        return max_val

    ## Game Move Methods
    def make_move(self, direction) -> bool:
        grid, score = self.sim_move(direction)

        if not grid:
            raise Exception("Invalid move in 'move' function")

        moved = self.grid != grid

        if not moved:
            print("No Changes")
            return False

        self.grid = grid
        self.score += score

        self.moves += 1
        self.spawnTile()

        return True

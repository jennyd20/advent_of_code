from typing import assert_type


DIR_ORTHOG = {"n": (-1, 0), "s": (1, 0), "w": (0, -1), "e": (0, 1)}
DIR_DIAG = {"ne": (-1, 1), "se": (1, 1), "nw": (-1, -1), "sw": (1, -1)}
DIR = DIR_DIAG | DIR_ORTHOG

CLOCKWISE = {"n": "e", "e": "s", "s": "w", "w": "n"}
COUNTER = {val: key for key, val in CLOCKWISE.items()}


class Grid:
    def __init__(self, input=""):
        self.input = input
        self.items = input.splitlines()
        self.max_rows = len(self.items)
        self.max_cols = len(self.items[0]) if self.max_rows else 0

    def __repr__(self):
        return f"Grid of size {self.max_rows}, {self.max_cols}"

    def copy(self):
        grid_copy = Grid()
        grid_copy.items = self.items.copy()
        grid_copy.max_rows = self.max_rows
        grid_copy.max_cols = self.max_cols
        return grid_copy

    def get_val(self, pos):
        if pos.out_of_bounds(self):
            raise OutOfBoundsError(f"Position {pos} out of bounds")
        return self.items[pos.row][pos.col]

    def set_val(self, pos, val):
        if pos.out_of_bounds(self):
            raise OutOfBoundsError(f"Position {pos} out of bounds")
        new_row = self.items[pos.row]
        new_row = new_row[: pos.col] + val + new_row[pos.col + 1 :]
        self.items[pos.row] = new_row
        return self

    def find_first_val(self, val):
        for p in self.all_pos():
            if val == self.get_val(p):
                return p
        raise ValueError(f"Value {val} not found in the grid")

    def all_pos(self):
        all_p = []
        for row in range(self.max_rows):
            for col in range(self.max_cols):
                all_p.append(Position(row, col))
        return all_p

    def dir_list(self, just_orthogonal=False):
        if just_orthogonal:
            return DIR_ORTHOG
        else:
            return DIR

    def get_diag_pairs(self):
        return (("nw", "se"), ("ne", "sw"))


class Position:
    def __init__(self, row, col, dir=None):
        self.row = row
        self.col = col
        self.dir = dir

    def __add__(self, row_dir, col_dir):
        self.row += row_dir
        self.col += col_dir

    def __repr__(self):
        return f"Pos({self.row}, {self.col}); dir: {self.dir}"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Position):
            return False
        return self.row == value.row and self.col == value.col and self.dir == value.dir

    def __hash__(self):
        return hash((self.row, self.col, self.dir))

    def go_dir(self, dir):
        self.__add__(DIR[dir][0], DIR[dir][1])
        return self

    def forward(self):
        return self.go_dir(self.dir)

    def in_bounds(self, grid):
        return 0 <= self.row < grid.max_rows and 0 <= self.col < grid.max_cols

    def out_of_bounds(self, grid):
        return not self.in_bounds(grid)

    def copy(self):
        return Position(self.row, self.col, self.dir)

    def rotate(self, clockwise=True):
        assert self.dir
        # TODO: implement non-orthogonal case
        if clockwise:
            self.dir = CLOCKWISE[self.dir]
        else:
            self.dir = COUNTER[self.dir]

    def get_coords(self):
        return self.row, self.col


class OutOfBoundsError(ValueError):
    "Attempted to access a position out of grid bounds"
    pass

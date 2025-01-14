DIR = {
    "n": (-1, 0),
    "s": (1, 0),
    "w": (0, -1),
    "e": (0, 1),
    "ne": (-1, 1),
    "se": (1, 1),
    "nw": (-1, -1),
    "sw": (1, -1),
}


class Grid:
    def __init__(self, input):
        self.rows = input.splitlines()
        self.max_rows = len(self.rows)
        self.max_cols = len(self.rows[0])

    def __repr__(self):
        return f"Grid of size {self.max_rows}, {self.max_cols}"

    def get_val(self, pos):
        if pos.out_of_bounds(self):
            raise ValueError(f"Position {pos} out of bounds")
        return self.rows[pos.row][pos.col]

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
    
    def dir_list(self, just_orthogonal = False):
        if just_orthogonal:
            return DIR[:3]
        else:
            return DIR
        
    def get_diag_pairs(self):
        return (("nw", "se"), ("ne", "sw"))

# TODO: use the grid class use the POS class
class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __add__(self, row_dir, col_dir):
        self.row += row_dir
        self.col += col_dir

    def __repr__(self):
        return f"({self.row}, {self.col})"

    def go_dir(self, dir):
        self.__add__(DIR[dir][0], DIR[dir][1])
        return self

    def out_of_bounds(self, grid):
        return not (0 <= self.row < grid.max_rows and 0 <= self.col < grid.max_cols)
    
    def duplicate(self):
        return Position(self.row, self.col)
    

from __future__ import annotations
from collections.abc import Callable
import enum
import dataclasses


class Dir(enum.Enum):
    N = (-1, 0)
    NE = (-1, 1)
    E = (0, 1)
    SE = (1, 1)
    S = (1, 0)
    SW = (1, -1)
    W = (0, -1)
    NW = (-1, -1)

    def is_orthog(self):
        row, col = self.value
        return row == 0 or col == 0

    def clockwise(self):
        row, col = self.value
        new_col = -row
        new_row = col
        return Dir((new_row, new_col))


DIR = set(Dir)
DIR_ORTHOG = {d for d in Dir if d.is_orthog()}
DIR_DIAG = {d for d in Dir if not d.is_orthog()}
DIR_DIAG_PAIRS = [(Dir.NW, Dir.SE), (Dir.NE, Dir.SW)]


@dataclasses.dataclass
class Grid[T]:
    input: str
    items: list[list[T]]
    max_rows: int
    max_cols: int

    @classmethod
    def create_from_input(
        cls, input: str, new_type: Callable[[str], T] = str
    ) -> Grid[T]:
        rows = input.splitlines()
        items = []
        for r in rows:
            row_to_list = [new_type(x) for x in r]
            items.append(row_to_list)
        return cls(input, items, len(rows), len(rows[0]))

    def __repr__(self):
        return f"Grid of size {self.max_rows}, {self.max_cols}"

    def get_val(self, pos: Position) -> T:
        if pos.out_of_bounds(self):
            raise ValueError(f"Position {pos} out of bounds")
        return self.items[pos.row][pos.col]

    def set_val(self, pos: Position, val) -> None:
        if pos.out_of_bounds(self):
            raise ValueError(f"Position {pos} out of bounds")
        new_row = self.items[pos.row]
        new_row = new_row[: pos.col] + [val] + new_row[pos.col + 1 :]
        self.items[pos.row] = new_row

    def get_all_val_pos(self, val:T) -> set[Position]:
        pos = set()
        for p in self.all_pos_iter():
            if val == self.get_val(p):
                pos.add(p)
        return pos

    def set_all_val_pos(self, val, pos: set[Position]):
        for p in pos:
            self.set_val(p, val)

    def get_first_val(self, val) -> Position:
        for p in self.all_pos_iter():
            if val == self.get_val(p):
                return p
        raise ValueError(f"Value {val} not found in the grid")

    def get_unique_vals(self) -> set[T]:
        return set(self.get_val(p) for p in self.all_pos_iter())

    def to_dict(self) -> dict[T, set[Position]]:
        all_vals = {}
        for p in self.all_pos_iter():
            v = self.get_val(p)
            val_pos = all_vals.get(v, set())
            val_pos.add(p)
            all_vals[v] = val_pos
        return all_vals

    def all_pos_iter(self):
        for row in range(self.max_rows):
            for col in range(self.max_cols):
                yield Position(row, col)

    def print(self):
        print()
        for row in self.items:
            print("".join(str(x) for x in row))
        print()


@dataclasses.dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __repr__(self):
        return f"({self.row}, {self.col})"

    def go_dir(self, dir: Dir) -> Position:
        dr, dc = dir.value
        return Position(self.row + dr, self.col + dc)

    def in_bounds(self, grid) -> bool:
        return 0 <= self.row < grid.max_rows and 0 <= self.col < grid.max_cols

    def out_of_bounds(self, grid) -> bool:
        return not self.in_bounds(grid)
    
    def get_orthog_pos(self, grid:Grid) -> set:
        orthog_pos = set()
        for d in DIR_ORTHOG:
            new_pos = self.go_dir(d)
            if new_pos.in_bounds(grid):
                orthog_pos.add(new_pos)
        return orthog_pos


@dataclasses.dataclass(frozen=True)
class PositionAndDirection:
    pos: Position
    dir: Dir

    def forward(self) -> PositionAndDirection:
        return PositionAndDirection(self.pos.go_dir(self.dir), self.dir)

    def rotate(self, clockwise=True) -> PositionAndDirection:
        assert self.dir
        # TODO: implement non-orthogonal case
        return PositionAndDirection(self.pos, self.dir.clockwise())

"""
Connect 4
"""

from typing import List
import numpy as np


EMPTY_CELL = '-'
COLORS = 'gr' + EMPTY_CELL


def is_winning_row(row: str, amount_to_win=4) -> bool:
    """Given a row, return True if there are enough adjacent pieces of the same player"""
    for c in COLORS:
        if c * amount_to_win in row:
            return True


class Board:
    """The board"""
    def __init__(self, rows: List[str]=None, size=(6, 7)):
        self.size = size
        if rows:
            self._np_array = np.array([list(row) for row in rows])
        else:
            self._np_array = np.full(self.size, EMPTY_CELL)

    @property
    def rows(self):
        return self._np_array.tolist()

    @property
    def columns(self):
        return self._np_array.transpose().tolist()

    @property
    def diagonals(self):
        diagonals = [self._np_array[::-1, :].diagonal(i)
                     for i in range(-self._np_array.shape[0] + 1, self._np_array.shape[1])]
        diagonals.extend(self._np_array.diagonal(i)
                         for i in range(self._np_array.shape[1] - 1, -self._np_array.shape[0], -1))

        return [d.tolist() for d in diagonals]

    def __iter__(self):
        """Iterate through all the lines, columns and diagonals on the board"""
        for row in self.rows:
            yield row
        for col in self.columns:
            yield col
        for diagon in self.diagonals:
            yield diagon

    def __len__(self) -> int:
        """Return the amount of cells on the board"""
        return self._np_array.size

    def __eq__(self, other) -> bool:
        return np.array_equal(self.rows, other.rows)

    def __str__(self) -> str:
        """Return the rows as a string"""
        return "\n".join([''.join(row) for row in self.rows])

    def __repr__(self) -> str:
        s = [''.join(row) for row in self._np_array]
        return f"<Board({s})>"


class Game:
    def __init__(self, board: Board, amount_to_win=4):
        """A game of connect 4"""
        self.board = board
        self.amount_to_win = amount_to_win

    def has_moves_left(self) -> bool:
        """Return true if there at least one EMPTY_CELL on the board"""
        return EMPTY_CELL in self.board._np_array

    def is_won(self) -> bool:
        """Return true if a winning line is found"""
        lines = list(self.board)
        return any([is_winning_row(''.join(line), self.amount_to_win) for line in lines])

    def is_draw(self) -> bool:
        """Return true if there are no move left and game was not won"""
        return not any([self.has_moves_left(), self.is_won()])

    # def get_row(self, column) -> int:
    #     for i, row in enumerate(self.board.rows):
    #         if row[column] == EMPTY_CELL:
    #             return i
    #
    # def move(self, column: int) -> None:
    #     rows = self.board.rows
    #     n = self.get_row(column)
    #     rows[n] = rows[n][:column] + '1' + rows[n][column + 1:]
    #     self.board = Board(rows)

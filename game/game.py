"""
Connect 4
"""

from typing import List
import numpy as np

from .exceptions import CellIsNotEmpty, GameOver


EMPTY_CELL = '-'
COLORS = 'gr'


def get_player_won(row: str, amount_to_win=4) -> str:
    """Given a row, return True if there are enough adjacent pieces of the same player"""
    for c in COLORS:
        if c * amount_to_win in row:
            return c


class Board:
    """The board"""
    def __init__(self, rows: List[str]=None, shape=(6, 7)):
        if rows:
            self._np_array = np.array([list(row) for row in rows])
            self.shape = self._np_array.shape
        else:
            self.shape = shape
            self._np_array = np.full(self.shape, EMPTY_CELL)

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

    def update_board(self, color: str, row: int, column: int):
        """update board only if the cell is valid and empty

        Will raise IndexError if given an invalid row or column
        Will raise CellIsNotEmpty is the cell is not empty
        """
        if self._np_array[row][column] == EMPTY_CELL:
            self._np_array[row][column] = color
        else:
            raise CellIsNotEmpty

    def is_full(self) -> bool:
        """Return True if there are no EMPTY_CELL cells on the board"""
        return EMPTY_CELL not in self._np_array

    def get_column(self, column):
        """Return the column"""
        return self._np_array[:, column]

    def get_empty_row_number(self, column):
        for i, v in enumerate(reversed(self.get_column(column))):
            if v == EMPTY_CELL:
                return self.shape[0] - 1 - i

        raise IndexError

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
        """Return True if two boards are equal"""
        return np.array_equal(self.rows, other.rows)

    def __str__(self) -> str:
        """Return the rows as a string"""
        return "\n".join([''.join(row) for row in self.rows])

    def __repr__(self) -> str:
        s = [''.join(row) for row in self._np_array]
        return f"<Board({s})>"


class Game:
    def __init__(self, board: Board = Board(), amount_to_win=4):
        """A game of connect 4"""
        self.board = board
        self.amount_to_win = amount_to_win

    def player_won(self) -> str:
        """Return the winning player, if found"""
        for line in self.board:
            c = get_player_won(''.join(line), self.amount_to_win)
            if c:
                return c

    def is_draw(self) -> bool:
        """Return True if there are no move left and game was not won"""
        return self.board.is_full() and not self.player_won()

    def get_player_to_move(self) -> str:
        """Return the color of the player that is next to move"""
        if (len(self.board) - str(self.board.rows).count(EMPTY_CELL)) % 2 == 0:
            return 'r'
        return 'g'

    def drop_piece(self, column):
        """Make a move If the game is over, raise GameOver
        """
        if self.player_won() or self.is_draw():
            raise GameOver

        p = self.get_player_to_move()
        row = self.board.get_empty_row_number(column)
        self.board.update_board(p, row, column)

        if self.player_won() or self.is_draw():
            raise GameOver

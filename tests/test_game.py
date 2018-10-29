import pytest
from itertools import product

from game.game import get_player_won, COLORS, Board, Game, EMPTY_CELL
from game.exceptions import CellIsNotEmpty, GameOver

rows = ["".join(row) for row in (list(product(COLORS, repeat=6)))]

winning_rows = [row for c in COLORS for row in rows if c * 4 in row]
not_winning_rows = [row for row in rows if row not in winning_rows]


def test_rows():
    assert len(rows) == len(winning_rows) + len(not_winning_rows)


def test_winning_rows():
    for row in winning_rows:
        assert get_player_won(row)


def test_not_winning_rows():
    for row in not_winning_rows:
        assert not get_player_won(row)


class TestStr:
    def test_one_cell(self):
        b = Board([EMPTY_CELL])
        assert b.__str__() == EMPTY_CELL

    def test_many_cells(self):
        b = Board(['rr', 'gg'])
        assert b.__str__() == 'rr\ngg'


class TestRepr:
    def test_one_cell(self):
        b = Board([EMPTY_CELL])
        assert b.__repr__() == f"<Board(['{EMPTY_CELL}'])>"

    def test_many_cells(self):
        b = Board(['rr', 'gg'])
        assert b.__repr__() == f"<Board(['rr', 'gg'])>"


class TestBoardEquality:
    """This also tests creation"""
    def test_default_board(self):
        b = Board()
        b2 = Board([])
        assert b == b2

    def test_unqual_boards(self):
        b = Board(['r'])
        b2 = Board(['g'])
        assert b != b2

    def test_equal_boards(self):
        b = Board(['g'])
        b2 = Board(['g'])
        assert b == b2


class TestBoardLen:
    def test_default_board(self):
        b = Board()
        assert len(b) == 42

    def test_custom_board(self):
        board = [EMPTY_CELL * 12 for _ in range(6)]
        b = Board(board)
        assert len(b) == 72


class TestColumns:
    def test_default(self):
        b = Board(shape=(1, 2))
        b2 = Board(shape=(2, 1))
        assert str(b.rows) == str(b2.columns)


class TestDiagonals:
    def test_diagonals(self):
        b = Board()
        assert len(b.diagonals) == (b.shape[0] + b.shape[1] - 1) * 2

    def test_one_diagonal(self):
        board = [EMPTY_CELL]
        b = Board(board)
        assert b.diagonals == [[EMPTY_CELL], [EMPTY_CELL]]

    def test_many_diagonals(self):
        board = [
            EMPTY_CELL * 3,
            ''.join(['g', 'r', EMPTY_CELL])
        ]
        b = Board(board)
        assert b.diagonals == [[EMPTY_CELL], ['g', EMPTY_CELL], ['r', EMPTY_CELL], [EMPTY_CELL], [EMPTY_CELL],
                               [EMPTY_CELL, EMPTY_CELL], [EMPTY_CELL, 'r'], ['g']]


class TestIter:
    def test_len(self):
        b = Board()
        assert len(list(b)) == len(b.columns) + len(b.rows) + len(b.diagonals)

    def test_content(self):
        board = [
            EMPTY_CELL * 3,
            ''.join(['g', 'r', EMPTY_CELL])
        ]
        b = Board(board)
        assert list(b) == b.rows + b.columns + b.diagonals


class TestBoardIsFull:
    def test_board_is_full(self):
        b = Board(['g'])
        assert b.is_full()

    def test_board_has_empty_cells(self):
        b = Board()
        assert not b.is_full()


class TestGameWon:
    def test_green_player_won(self):
        board = ['gggg']
        g = Game(board=Board(board))
        assert g.player_won() == 'g'

    def test_red_player_won(self):
        board = ['rrrr']
        g = Game(board=Board(board))
        assert g.player_won() == 'r'

    def test_game_not_won(self):
        g = Game(Board(['ggrg']))
        assert not g.player_won()


class TestIsDraw:
    def test_has_moves_not_won(self):
        b = Board([EMPTY_CELL])
        g = Game(b)
        assert not g.is_draw()

    def test_no_moves_not_won(self):
        b = Board(['r'])
        g = Game(b)
        assert g.is_draw()

    def test_no_moves_won(self):
        board = [
            'gggg'
        ]
        b = Board(board)
        g = Game(b)
        assert not g.is_draw()

    def test_has_moves_won(self):
        board = [
            EMPTY_CELL * 7,
            EMPTY_CELL * 7,
            EMPTY_CELL * 7,
            EMPTY_CELL * 7,
            EMPTY_CELL * 7,
            EMPTY_CELL + 'rrr' + EMPTY_CELL * 3,
            EMPTY_CELL + 'gggg' + EMPTY_CELL * 2,
        ]
        g = Game(board=Board(board))
        assert not g.is_draw()


class TestUpdateBoard:
    def test_one_dimensional_board(self):
        b = Board([EMPTY_CELL * 7])
        b.update_board(color='r', row=0, column=0)
        assert b == Board(['r' + EMPTY_CELL * 6])

    def test_two_dimensional_board(self):
        b = Board([EMPTY_CELL * 2, EMPTY_CELL * 2])
        b.update_board(color='r', row=0, column=0)
        assert b == Board(['r-', '--'])

    def test_cell_is_taken(self):
        b = Board([EMPTY_CELL])
        b.update_board(color='r', row=0, column=0)
        with pytest.raises(CellIsNotEmpty):
            b.update_board(color='g', row=0, column=0)

    def test_invalid_index(self):
        b = Board([EMPTY_CELL])
        with pytest.raises(IndexError):
            b.update_board(color='g', row=1, column=0)


class TestPlayerTurn:
    def test_odd_move(self):
        g = Game(Board())
        assert g.get_player_to_move() == 'r'

    def test_even_move(self):
        g = Game(Board(['-r']))
        assert g.get_player_to_move() == 'g'


class TestMove:
    def test_move_no_draw_no_win(self):
        g = Game(Board(['--']))
        # g.drop_piece(column=0)
        assert g.board.shape == (1, 2)

    def test_move_after_won(self):
        g = Game(Board(['rrrr']))
        with pytest.raises(GameOver):
            g.drop_piece(0)

    def test_move_leading_to_win(self):
        g = Game(Board(['ggg-', 'rrr-']))
        with pytest.raises(GameOver):
            g.drop_piece(3)

    def test_move_after_drawn(self):
        g = Game(Board(['r']))
        with pytest.raises(GameOver):
            g.drop_piece(0)

    def test_move_leading_to_draw(self):
        g = Game(Board(['-']))
        with pytest.raises(GameOver):
            g.drop_piece(0)


class TestGetEmptyRowNumber:
    def test_valid_row(self):
        b = Board(['-'])
        assert b.get_empty_row_number(0) == 0

    def test_invalid_row(self):
        b = Board(['r'])
        with pytest.raises(IndexError):
            b.get_empty_row_number(0)

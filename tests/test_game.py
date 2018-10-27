from itertools import product

from game.game import is_winning_row, COLORS, Board, Game, EMPTY_CELL

rows = ["".join(row) for row in (list(product(COLORS, repeat=6)))]

winning_rows = [row for c in COLORS for row in rows if c * 4 in row]
not_winning_rows = [row for row in rows if row not in winning_rows]


def test_rows():
    assert len(rows) == len(winning_rows) + len(not_winning_rows)


def test_winning_rows():
    for row in winning_rows:
        assert is_winning_row(row)


def test_not_winning_rows():
    for row in not_winning_rows:
        assert not is_winning_row(row)


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
        b = Board(size=(1, 2))
        b2 = Board(size=(2, 1))
        assert str(b.rows) == str(b2.columns)


class TestDiagonals:
    def test_diagonals(self):
        b = Board()
        assert len(b.diagonals) == (b.size[0] + b.size[1] - 1) * 2

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


class TestGame:
    def test_has_moves_left(self):
        b = Board([EMPTY_CELL])
        g = Game(b)
        assert g.has_moves_left()
        b = Board(['g'])
        g = Game(b)
        assert not g.has_moves_left()

    def test_game_won(self):
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
        assert g.is_won()


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


# class TestMove:
#     def test_something(self):
#         board = ['-']
#         b = Board(board)
#         g = Game(b)
#         g.move(7)
#         assert g.board == Board(['1'])

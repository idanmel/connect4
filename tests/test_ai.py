import pytest

from game.game import Board, is_column_full, EMPTY_CELL, get_possible_moves
from ai.bots import get_random_column, get_winning_column, RandomBot


class TestGetRandomColumn:
    def test_range(self):
        assert 6 >= get_random_column() >= 0


class TestGetWinningColumn:
    def test_win(self):
        b = Board(['ggg-'])
        columns = [3]
        assert get_winning_column(b, columns) == 3

    def test_no_win(self):
        b = Board(['rrr-'])
        columns = [3]
        assert not get_winning_column(b, columns)


class TestGetOpponentWinningColumn:
    def test_no_win(self):
        b = Board(['ggg-'])
        columns = [3]
        assert not get_winning_column(b, columns, opponent=True)

    def test_win(self):
        b = Board(['rrr-'])
        columns = [3]
        assert get_winning_column(b, columns, opponent=True) == 3


class TestRandomBot:
    def test_random_bot(self):
        r = RandomBot()
        assert type(r.get_column()) == int


class TestIsColumnFull:
    def test_full_column(self):
        b = Board(['g'])
        c = b.get_column(0)
        assert is_column_full(c)

    def test_not_full_column(self):
        b = Board([EMPTY_CELL])
        c = b.get_column(0)
        assert not is_column_full(c)


class TestFindPossibleMoves:
    def test_zero_moves(self):
        b = Board(['g'])
        assert get_possible_moves(b) == []

    def test_one_move(self):
        b = Board(['-'])
        assert len(get_possible_moves(b)) == 1

    def test_multiple_moves(self):
        b = Board([
            '--',
            'g-'
        ])
        assert len(get_possible_moves(b)) > 1

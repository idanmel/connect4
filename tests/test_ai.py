from game.game import Board, Game, is_column_full, EMPTY_CELL, get_possible_moves


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


# class TestGetWinningMove:
#     def test_one_winning_move(self):
#         g = Game(Board(['ggg-', 'rrr-']))
#         assert get_winning_move(g) == 3
#
#     def test_zero_winning_moves(self):
#         g = Game(Board(['----']))
#         assert get_winning_move(g) == 4

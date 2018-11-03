import random
import timeit

from typing import List
from game.game import get_possible_moves, Game, Board, Player
from game.exceptions import GameWon, GameDrawn


def get_random_column(number_of_columns=7) -> int:
    return random.randint(0, number_of_columns - 1)


def get_winning_column(board: Board, columns: List[int], opponent=False):
    copied_board = board.rows
    for column in columns:
        g = Game(board=Board(rows=copied_board))
        try:
            color = g.get_color_to_move()
            if opponent:
                color = g.get_opponent_color()
            g.make_move(column, color)
        except GameDrawn:
            continue
        except GameWon:
            return column


class RandomBot(Player):

    def get_column(self, board=None):
        return get_random_column()


class Monte(Player):

    def __init__(self, number_of_games=4000):
        self.number_of_games = number_of_games
        Player.__init__(self)

    def get_random_game_result(self, board, column) -> bool:
        board_copy = board.rows
        g = Game(player1=RandomBot(), player2=RandomBot(), board=Board(rows=board_copy))
        my_color = g.current_color
        try:
            g.make_move(column)
        except GameDrawn:
            return False
        except GameWon:
            return True
        while True:
            try:
                g.make_move()
            except IndexError:
                pass
            except GameDrawn:
                return False
            except GameWon:
                return g.current_color == my_color

    def get_column(self, board=None) -> int:

        print("\n*** Hmmm... Let me think... ***")
        if not board:
            board = Board()

        columns = get_possible_moves(board)
        column = get_winning_column(board, columns)
        if column:
            return column

        column = get_winning_column(board, columns, opponent=True)
        if column:
            return column

        games_per_column = self.number_of_games // len(columns)
        win_rate = []
        for column in columns:
            results = [self.get_random_game_result(board, column) for _ in range(games_per_column)]
            win_rate.append((results.count(True), column))

        return max(win_rate)[1]


if __name__ == '__main__':
    m = Monte()
    tries = 10
    print(timeit.timeit(m.get_column, number=tries) / tries)

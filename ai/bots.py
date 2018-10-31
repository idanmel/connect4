import random
from game.game import get_possible_moves, Game, Board
from game.exceptions import GameWon, GameDrawn


def get_random_column(number_of_columns=7) -> int:
    return random.randint(0, number_of_columns - 1)


def get_random_game_result(board, column) -> bool:
    copied_board = board.rows
    g = Game(Board(rows=copied_board))
    try:
        g.drop_piece(column)
    except GameDrawn:
        return False
    except GameWon:
        return True
    while True:
        try:
            column = get_random_column(g.board.shape[1])
            g.drop_piece(column)
        except IndexError:
            pass
        except GameDrawn:
            return False
        except GameWon:
            return g.get_player_to_move() == 'g'


def found_opponent_winning_move(board, column):
    copied_board = board.rows
    g = Game(Board(rows=copied_board))
    try:
        g.drop_piece(column, invert_player=True)
    except GameDrawn:
        return False
    except GameWon:
        return True


class Monte:

    @staticmethod
    def get_best_column(board, number_of_games=1000) -> int:

        columns = get_possible_moves(board)
        for column in columns:
            if found_opponent_winning_move(board, column):
                return column

        games_per_column = number_of_games // len(columns)
        winrate = []
        for column in columns:
            wins = 0
            for i in range(games_per_column):
                result = get_random_game_result(board, column)
                if result:
                    wins += 1
            winrate.append((wins, column))

        return max(winrate)[1]



# def get_winning_move(g):
#     winning_columns = []
#     for column in range(g.board.shape[1]):
#         g.drop_piece(column)
#         if g.player_won():
#             winning_columns.append(column)
#
#     return winning_columns

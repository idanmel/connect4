import random
from game.game import get_possible_moves, Game
from game.exceptions import GameWon, GameDrawn

def get_random_column(number_of_columns=7):
    return random.randint(0, number_of_columns - 1)


def won_random_game(board, column):
    g = Game(board)
    g.drop_piece(column)
    while True:
        try:
            g.drop_piece(get_random_column)
        except IndexError:
            pass
        except GameDrawn:
            return False
        except GameWon:
            return g.player_won() == 'r'


class Monte:

    @staticmethod
    def get_best_column(board, number_of_games=1000):
        winrate = []
        columns = get_possible_moves(board)
        games_per_column = number_of_games // len(columns)
        for column in columns:
            wins = 0
            for i in range(games_per_column):
                if won_random_game(board, column):
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

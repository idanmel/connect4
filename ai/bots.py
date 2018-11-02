import random
from game.game import get_possible_moves, Game, Board, Player
from game.exceptions import GameWon, GameDrawn


def get_random_column(number_of_columns=7) -> int:
    return random.randint(0, number_of_columns - 1)


def found_opponent_winning_move(board, column):
    copied_board = board.rows
    g = Game(board=Board(rows=copied_board))
    try:
        g.make_move(column, color=g.get_opponent_color())
    except GameDrawn:
        return False
    except GameWon:
        return True


class RandomBot(Player):

    def get_column(self, board=None):
        return get_random_column()


class Monte(Player):

    def __init__(self, number_of_games=5000):
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

        columns = get_possible_moves(board)
        for column in columns:
            if found_opponent_winning_move(board, column):
                return column

        games_per_column = self.number_of_games // len(columns)
        win_rate = []
        for column in columns:
            wins = 0
            for i in range(games_per_column):
                result = self.get_random_game_result(board, column)
                if result:
                    wins += 1
            win_rate.append((wins, column))

        return max(win_rate)[1]

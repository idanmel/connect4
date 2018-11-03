from game.game import Game, HumanPlayer, Player
from game.exceptions import GameDrawn, GameWon
from ai.bots import Monte, RandomBot
import argparse


def get_players():
    bot_options = {
        'human': HumanPlayer,
        'random': RandomBot,
        'monte': Monte
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('p1', help="Choose the first player", choices=bot_options.keys())
    parser.add_argument('p2', help="Choose the second player", choices=bot_options.keys())
    args = parser.parse_args()

    return bot_options[args.p1](), bot_options[args.p2]()


def play_game(player1: Player = HumanPlayer(), player2: Player=Monte()):

    g = Game(player1, player2)
    print("\n" + str(g.board))
    while True:
        try:
            g.make_move()
        except (ValueError, IndexError):
            print('\n*** Please choose your move again ***')
        except GameDrawn:
            print("\n*** Game ended in a draw ***")
            return
        except GameWon:
            print(f"\n*** {g.current_color} won!!! ***")
            return
        except (KeyboardInterrupt, EOFError):
            print("\nWhat did you do that for?")
            return
        finally:
            print("\n" + str(g.board))


if __name__ == '__main__':
    player_one, player_two = get_players()
    play_game(player_one, player_two)

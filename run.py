from game.game import Game, HumanPlayer
from game.exceptions import GameDrawn, GameWon
from ai.bots import Monte


def run():

    g = Game(player1=Monte(number_of_games=7), player2=HumanPlayer())
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
    run()

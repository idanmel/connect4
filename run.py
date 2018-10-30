from game.game import Game
from game.exceptions import GameDrawn, GameWon
from ai.bots import Monte


def run():
    g = Game()
    while True:
        try:
            p = g.get_player_to_move()
            if p == 'r':
                print('\n*** Let me think... ***')
                column = Monte.get_best_column(board=g.board, number_of_games=5000)
            else:
                column = int(input("Enter Column: ")) - 1
            g.drop_piece(column)
        except (ValueError, IndexError):
            print('\n*** Please choose your move again ***')
        except GameDrawn:
            print("\n*** Game ended in a draw ***")
            return
        except GameWon:
            print(f"\n*** {p} won!!! ***")
            return
        except (KeyboardInterrupt, EOFError):
            print("\nWhat did you do that for?")
            return
        finally:
            print("\n" + str(g.board))


if __name__ == '__main__':
    run()

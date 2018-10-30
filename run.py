from game.game import Game
from game.exceptions import GameDrawn, GameWon
from ai.bots import Monte


def run():
    g = Game()
    while True:
        try:
            p = g.get_player_to_move()
            if p == 'r':
                column = Monte.get_best_column(board=g.board, number_of_games=10)
            else:
                column = int(input("Enter Column: "))
                print("\n*** Aha! Now I'll get you! ***")
            g.drop_piece(column)
        except (ValueError, IndexError):
            print('\n*** Please choose your move again ***')
        except GameDrawn:
            print("\n*** Game ended in a draw ***")
            return
        except GameWon:
            print(f"\n*** {g.player_won()} won!!! ***")
            return
        except (KeyboardInterrupt, EOFError):
            print("\nWhat did you do that for?")
            return
        finally:
            print(g.board)


if __name__ == '__main__':
    run()

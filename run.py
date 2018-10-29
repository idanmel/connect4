from game.game import Game
from game.exceptions import GameDrawn, GameWon


def run():
    g = Game()
    while True:
        try:
            column = int(input("Enter Column: "))
            g.drop_piece(column)
        except (ValueError, IndexError):
            print('\n***Please choose your move again***')
        except GameDrawn:
            print("\n***Game finished in draw")
            return
        except GameWon:
            print(f"\n***{g.player_won()} won!!!***")
            return
        except (KeyboardInterrupt, EOFError):
            print("\nWhat did you do that for?")
            return
        finally:
            print(g.board)


if __name__ == '__main__':
    run()

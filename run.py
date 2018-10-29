from game.game import Game
from game.exceptions import GameOver

g = Game()
while True:
    try:
        column = int(input("Enter Column: "))
        g.drop_piece(column)
    except (ValueError, IndexError):
        print('\n***Please choose your move again***')
    except GameOver:
        if g.is_draw():
            print("\n***Game finished in draw")
        else:
            print(f"\n***{g.player_won()} won!!!***")
        break
    except (KeyboardInterrupt, EOFError):
        print("\nWhat did you do that for?")
        exit(1)
    finally:
        print(g.board)

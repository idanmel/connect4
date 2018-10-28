from game.game import Game
from game.exceptions import CellIsNotEmpty, GameOver

g = Game()
while True:
    try:
        row = int(input("Row: "))
        column = int(input("Column: "))
        g.move(row, column)
    except (CellIsNotEmpty, ValueError, IndexError):
        print('\n***Please choose your move again***')
    except (GameOver, KeyboardInterrupt):
        if g.is_draw():
            print("\n***Game finished in draw")
        else:
            print(f"\n***{g.player_won()} won!!!***")
        break
    finally:
        print(g.board)

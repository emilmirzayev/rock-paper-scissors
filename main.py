from rps.game import Game


def main():
    g = Game()
    while g.gameContinue:
        g._update_game_process()
    print()
    print()
    print("This screen will close in 30 seconds or when you close it")
    g._announce_game_results()
    

main()
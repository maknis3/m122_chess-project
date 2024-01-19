from game import ChessGame
import cProfile

if __name__ == "__main__":
    game = ChessGame()
    game.start_game()
    #cProfile.run("game.start_game()", "profile_output") #bash: snakeviz profile_output.prof
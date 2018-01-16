from RandomPlayer import RandomPlayer
from EdgePlayer import EdgePlayer
from data_structures.types import GameState


def main():
    # Instantiate the game state
    gamestate = GameState(_,_,10,5)

    # Initialize a concrete class for player 1 and run the placepoints method
    player1 = RandomPlayer(1, gamestate)
    gamestate = player1.placepoints

    # Initialize a concrete class for player 2 and run the placepoints method
    player2 = RandomPlayer(2, gamestate)
    gamestate = player2.placepoints

    # Visualize the result

from RandomPlayer import RandomPlayer
from EdgePlayer import EdgePlayer


def main():
    # Instantiate the game state
    gamestate = {'width': 100, 'height': 100, 'm': 10, 'n': 5, 'points': []}

    # Initialize a concrete class for player 1 and run the placepoints method
    player1 = RandomPlayer(1, gamestate)
    player1.placepoints()

    # Initialize a concrete class for player 2 and run the placepoints method
    player2 = RandomPlayer(2, gamestate)
    player2.placepoints()

    # Visualize the result

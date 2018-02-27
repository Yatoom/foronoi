from Visualization import Visualization
from algorithm import Algorithm
from graph import BoundingBox
from voronoi_players.IntersectionPlayer_Multi import IntersectionPlayer
from voronoi_players.gamestate import GameState
from voronoi_players.pattern_players import SquarePlayer


def main():
    # Instantiate the game state
    state = GameState(width=25, height=25, m=16, n=15)

    # Initialize a concrete class for player 1 and run the place_points method
    player1 = SquarePlayer(1, state)
    state = player1.place_points
    print('test')
    print(state.points)
    # Initialize a concrete class for player 2 and run the place_points method
    player2 = IntersectionPlayer(2, state)
    print(player2)
    state = player2.place_points
    print(state)
    print('test')
    print(state.points)

    # # Visualize the result
    # voronoi = Voronoi()
    # v_diagram = voronoi.create_diagram(state.points)
    #
    #


    voronoi = Algorithm(BoundingBox(-0.1, 25.1, -0.1, 25.1))
    voronoi.create_diagram(state.points, visualize_steps=False)
    print(state.points)

    visualization = Visualization(state)
    name = 'visualization.svg'
    visualization.create_visualization(name)
    print('created visualiztion \n stored as: ' + name)

    score_p1, score_p2 = 0.0, 0.0

    for point in state.points:
        if point.player == 1:
            score_p1 += point.cell_size()
        else:
            score_p2 += point.cell_size()

    print("Player 1 score = {:.2f}".format(score_p1))
    print("Player 2 score = {:.2f}".format(score_p2))
    print("Score division = {:.1%}".format(score_p1 / (score_p1 + score_p2)))


main()

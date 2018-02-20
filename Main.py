from voronoi_players.pattern_players import SquarePlayer
from voronoi_players.pattern_players import SquareLongPlayer
from voronoi_players.pattern_players import TrianglePlayer
from voronoi_players.pattern_players import TriangleLongPlayer
from voronoi_players.pattern_players import CirclePlayer
from voronoi_players.pattern_players import LinePlayer
from voronoi_players.pattern_players import CircleCenterPlayer
from voronoi_players.random_players import NormalPlayer
from voronoi_players.IntersectionPlayer import IntersectionPlayer
from voronoi_players.EdgePlayer import EdgePlayer
from data_structures.types import GameState
from algorithm import Algorithm
from Visualization import Visualization
from nodes.bounding_box import BoundingBox


def main():
    # Instantiate the game state
    state = GameState(width=25, height=25, m=16, n=15)

    # Initialize a concrete class for player 1 and run the place_points method
    player1 = LinePlayer(1, state)
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



    voronoi = Algorithm(BoundingBox(0, 25, 0, 25))
    voronoi.create_diagram(state.points, visualize_steps=False)

    visualization = Visualization(state)
    name = 'visualization.svg'
    visualization.create_visualization(name)
    print('created visualiztion \n stored as: ' + name)

main()
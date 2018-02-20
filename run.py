from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from voronoi_players.pattern_players import LinePlayer as Player1
from voronoi_players.EdgePlayer import EdgePlayer as Player2
from data_structures.types import GameState


state = GameState(25,25,5,4)
player1 = Player1(1, state)
state = player1.place_points

player2 = Player2(2, state)
state = player2.place_points

v = Algorithm(BoundingBox(-1, 26, -1, 26))
v.create_diagram(points=state.points, visualize_steps=False, verbose=False)

score_p1, score_p2 = 0.0, 0.0

for point in state.points:
    if point.player == 1:
        score_p1 += point.cell_size()
    else:
        score_p2 += point.cell_size()

print("Player 1 score = {:.2f}".format(score_p1))
print("Player 2 score = {:.2f}".format(score_p2))
print("Score division = {:.1%}".format(score_p1/(score_p1 + score_p2)))

import svgwrite

from data_structures.types import GameState
from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from voronoi_players.abstract_player import Player


class Visualization(GameState):

    def __init__(self, state: GameState):
        self.state = state

    colour_bounding_box = svgwrite.rgb(0, 0, 0, '%')
    colour_edges = svgwrite.rgb(64, 64, 64, '%')
    colour_polygon_player_1 = svgwrite.rgb(255, 51, 51, '%')
    colour_point_player_1 = svgwrite.rgb(153, 0, 0, '%')
    colour_polygon_player_2 = svgwrite.rgb(102, 178, 255, '%')
    colour_point_player_2 = svgwrite.rgb(0, 76, 153, '%')
    colour_polygon_unknown = svgwrite.rgb(160, 160, 160, '%')
    colour_point_unknown = svgwrite.rgb(255, 255, 255, '%')

    strokewidth_bounding_box = '5'
    strokewidth_edges = '5'

    size_point = '1'

    def create_visualization(self, name):
        # Construct a Voronoi for the points in the GameState
        voronoi = Algorithm(BoundingBox(0, 25, 0, 25))
        voronoi.create_diagram(self.state.points, visualize_steps=False)

        # Check whether name has .svg extension
        if name[-4:] != '.svg':
            name = name + '.svg'

        # Initiate SVG image
        play_board = svgwrite.Drawing(name, profile='tiny')

        # For each vonoroi polygon, create a polygon
        edges_seen = []
        for edge in voronoi.edges:
            play_board.add(play_board.line((edge.origin.position.x, edge.origin.position.y), (edge.twin.origin.position.x, edge.twin.origin.position.y),
                                           stroke=self.colour_edges,
                                           stroke_width=self.strokewidth_edges))
            # Define the colour of the face
            if edge.incident_point.player == 1:
                colour_point = self.colour_point_player_1
            elif edge.incident_point.player == 2:
                colour_point = self.colour_point_player_2
            else:
                colour_point = self.colour_point_unknown

            # Add Point to SVG
            play_board.add(play_board.circle([edge.incident_point.x, edge.incident_point.y],
                                             fill=colour_point, r='1'))

        # Add bounding Box to SVG
        play_board.add(play_board.line((0, 0), (self.state.width, 0),
                                       stroke=self.colour_bounding_box,
                                       stroke_width=self.strokewidth_bounding_box))
        play_board.add(play_board.line((0, self.state.height), (self.state.width, self.state.height),
                                       stroke=self.colour_bounding_box,
                                       stroke_width=self.strokewidth_bounding_box))
        play_board.add(play_board.line((0, 0), (0, self.state.height),
                                       stroke=self.colour_bounding_box,
                                       stroke_width=self.strokewidth_bounding_box))
        play_board.add(play_board.line((self.state.width, 0), (self.state.width, self.state.height),
                                       stroke=self.colour_bounding_box,
                                       stroke_width=self.strokewidth_bounding_box))

        play_board.save()



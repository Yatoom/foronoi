import svgwrite

from data_structures.types import GameState
from fortune_algorithm import Voronoi


class Visualization:

    def __init__(self, player_nr: int, state: GameState):
        self.player_nr = player_nr
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
        voronoi = Voronoi()
        voronoi_diagram = voronoi.create_diagram(self.state.points)

        # Check whether name has .svg extension
        if name[-4:] != '.svg':
            name = name + '.svg'

        # Initiate SVG image
        play_board = svgwrite.Drawing(name, profile='tiny')

        # For each vonoroi polygon, create a polygon
        edges_seen = []
        for half_edge in voronoi_diagram:
            # Check whether any half-edge in the corresponding polygon has been seen before.
            if half_edge not in edges_seen:
                # Find all half edges corresponding to the current polygon
                half_edges_polygon = []
                half_edges_polygon.append(half_edge)
                half_edge_followup = half_edge.next
                while half_edge_followup != half_edge:
                    half_edges_polygon.append(half_edge_followup)
                    half_edge_followup = half_edge_followup.next

                # Create a list of all coordinates for the polygon
                polygon = []
                for edge in half_edges_polygon:
                    polygon.append([edge.origin.x, edge.origin.y])

                # Define the colour of the face
                if half_edge.inner_point.player == 1:
                    colour_polygon = self.colour_polygon_player_1
                    colour_point = self.colour_point_player_1
                elif half_edge.inner_point.player == 2:
                    colour_polygon = self.colour_polygon_player_2
                    colour_point = self.colour_point_player_2
                else:
                    colour_polygon = self.colour_polygon_unknown
                    colour_point = self.colour_point_unknown

                # Add Polygon to SVG
                play_board.add(play_board.polygon(polygon, fill=colour_polygon, stroke=self.colour_edges,
                                                  stroke_width=self.strokewidth_bounding_box))

                # Add Point to SVG
                play_board.add(play_board.circle([half_edge.inner_point.x, half_edge.inner_point.y],
                                                 fill=colour_point, stroke='None', r='1'))

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



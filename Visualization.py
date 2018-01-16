import svgwrite


class Visualization():

    def export_svg(self, name):
        # Check whether name has .svg extension
        if name[-4:] != '.svg':
            name = name + '.svg'

        # Initiate SVG image
        playBoard = svgwrite.Drawing(name, profile='tiny')

        # Add bounding Box
        colour = svgwrite.rgb(0, 0, 0, '%')
        playBoard.add(playBoard.line((0, 0),                 (self.state.width, 0),                 stroke=colour))
        playBoard.add(playBoard.line((0, self.state.height), (self.state.width, self.state.height), stroke=colour))
        playBoard.add(playBoard.line((0, 0),                 (0, self.state.height),                stroke=colour))
        playBoard.add(playBoard.line((self.state.width, 0),  (self.state.width, self.state.height), stroke=colour))

        # Add Voronoi Polygons
        colour_player1 = svgwrite.rgb(255, 0, 0, '%')
        colour_player2 = svgwrite.rgb(0, 0, 255, '%')

        for edge in 
        playBoard.defs.add(
            playBoard.polygon([(0, 0), (triangle_size, 0), (triangle_size, triangle_size)], id='triangle', fill='', stroke='none'))


from copy import copy
from decimal import Decimal

import numpy as np
from matplotlib import patches

from foronoi import Coordinate
from foronoi.algorithm import Algorithm
from foronoi.events import CircleEvent
import matplotlib.pyplot as plt


class Colors:
    SWEEP_LINE = "#2c3e50"
    VERTICES = "#34495e"
    BEACH_LINE = "#f1c40f"
    EDGE = "#636e72"
    ARC = "#95a5a6"
    INCIDENT_POINT_POINTER = "#ecf0f1"
    INVALID_CIRCLE = "#ecf0f1"  # red
    VALID_CIRCLE = "#2980b9"  # blue
    CELL_POINTS = "#bdc3c7"  # blue
    TRIANGLE = "#e67e22"  # orange
    BOUNDING_BOX = "black"  # blue
    TEXT = "#00cec9"  # green
    HELPER = "#ff0000"
    HIGH_LIGHT = "#00ff00"
    EDGE_DIRECTION = "#fdcb6e"
    FIRST_EDGE = "#2ecc71"


class Presets:
    # A minimalistic preset that is useful during construction
    construction = dict(polygon=True, events=True, beach_line=True, sweep_line=True)

    # A minimalistic preset that is useful during clipping
    clipping = dict(polygon=True)

    # A minimalistic preset that is useful to show the final result
    final = dict()


class Visualizer:
    """
    Visualizer
    """

    def __init__(self, voronoi, canvas_offset=1, figsize=(8, 8)):
        """
        A visualizer for your voronoi diagram.

        Examples
        --------
        Quickly plot individual components of the graph.

        >>> vis = Visualizer(voronoi, canvas_offset=1)
        >>> vis.plot_sites(show_labels=True)
        >>> vis.plot_edges(show_labels=False)
        >>> vis.plot_vertices()
        >>> vis.plot_border_to_site()
        >>> vis.show()

        Chaining commands

        >>> Visualizer(voronoi, 1).plot_sites().plot_edges().plot_vertices().show()

        Plot all components that are useful to visualize during construction of the diagram

        >>> from foronoi.visualization import Presets
        >>> Visualizer(voronoi, 1).plot_all(**Presets.construction)

        Plot all components that are useful to visualize when the diagram is constructed

        >>> Visualizer(voronoi, 1).plot_all()

        Parameters
        ----------
        voronoi: Voronoi
            The voronoi object
        canvas_offset: Int
            The space around the bounding object
        figsize: float, float
            Width, height in inches
        """
        self.voronoi = voronoi
        self.min_x, self.max_x, self.min_y, self.max_y = self._canvas_size(voronoi.bounding_poly, canvas_offset)
        plt.close("all")  # Prevents previous created plots from showing up
        fig, ax = plt.subplots(figsize=figsize)
        self.canvas = ax

    def _set_limits(self):
        self.canvas.set_ylim(self.min_y, self.max_y)
        self.canvas.set_xlim(self.min_x, self.max_x)
        return self

    def get_canvas(self):
        """
        Retrieve the figure.

        Returns
        -------
        Figure: matplotlib.figure.Figure
        """
        self._set_limits()
        return self.canvas.figure

    def show(self, block=True, **kwargs):
        """
        Display all open figures.

        Parameters
        ----------
        block : bool, optional

            If `True` block and run the GUI main loop until all windows
            are closed.

            If `False` ensure that all windows are displayed and return
            immediately.  In this case, you are responsible for ensuring
            that the event loop is running to have responsive figures.

        Returns
        -------
        self: Visualizer
        """
        self._set_limits()
        plt.show(block=block, **kwargs)
        return self

    def plot_all(self, polygon=False, edges=True, vertices=True, sites=True,
                 outgoing_edges=False, border_to_site=False, scale=1,
                 edge_labels=False, site_labels=False, triangles=False, arcs=False, sweep_line=False, events=False,
                 arc_labels=False, beach_line=False):
        """
        Convenience method that calls other methods to display parts of the diagram.

        Parameters
        ----------
        polygon: bool
            Display the polygon outline.
            *Only useful during construction.*
        edges: bool
            Display the borders of the cells.
        vertices: bool
            Display the intersections of the edges.
        sites: bool
            Display the cell points (a.k.a. sites)
        outgoing_edges: bool
            Show arrows of length `scale` in the direction of the outgoing edges for each vertex.
        border_to_site: bool
            Indicate with dashed line to which site a border belongs. The site's first edge is colored green.
        scale: float
            Used to set the length of the `outgoing_edges`.
        edge_labels: bool
            Display edge labels of format "`A/B`", where the edge is `A`'s border and the edge's twin is `B`'s border.
        site_labels: bool
            Display the labels of the cell points, of format "`P#`", where `#` is the `n`th point from top to bottom.
        triangles: bool
            Display the triangle of the 3 points responsible for causing a circle event.
            *Only useful during construction.*
        arcs: bool
            Display each arc for each point. Only used if `beach_line` is also `True`.
            *Only useful during construction.*
        sweep_line: bool
            Display the sweep line.
            *Only useful during construction.*
        events: bool
            Display circles for circle events.
            *Only useful during construction.*
        arc_labels: bool
            Display labels on the arcs.
            *Only useful during construction.*
        beach_line: bool
            Display the beach line.
            *Only useful during construction.*
        Returns
        -------
        self: Visualizer
        """

        self.plot_sweep_line() if sweep_line else False
        self.plot_polygon() if polygon else False
        self.plot_edges(show_labels=edge_labels) if edges else False
        self.plot_border_to_site() if border_to_site else False
        self.plot_vertices() if vertices else False
        self.plot_sites(show_labels=site_labels) if sites else False
        self.plot_outgoing_edges(scale=scale) if outgoing_edges else False
        self.plot_event(triangles) if events else False
        self.plot_arcs(plot_arcs=arcs, show_labels=arc_labels) if beach_line else False
        self._set_limits()
        return self

    def plot_polygon(self):
        """
        Display the polygon outline.
        *Only useful during construction.*

        Returns
        -------
        self: Visualizer
        """
        if hasattr(self.voronoi.bounding_poly, 'radius'):
            # Draw bounding box
            self.canvas.add_patch(
                patches.Circle((self.voronoi.bounding_poly.xd, self.voronoi.bounding_poly.xd),
                               self.voronoi.bounding_poly.radius,
                               fill=False,
                               edgecolor=Colors.BOUNDING_BOX)
            )
        else:
            # Draw bounding box
            self.canvas.add_patch(
                patches.Polygon(self.voronoi.bounding_poly.get_coordinates(), fill=False, edgecolor=Colors.BOUNDING_BOX)
            )

        return self

    def plot_vertices(self, vertices=None, **kwargs):
        """
        Display the intersections of the edges.

        Parameters
        ----------
        vertices: list(:class:`voronoi.graph.Vertex`), optional
            The vertices to display. By default, the `voronoi`'s vertices will be used.

        Returns
        -------
        self: Visualizer
        """
        vertices = vertices or self.voronoi.vertices

        xs = [vertex.xd for vertex in vertices]
        ys = [vertex.yd for vertex in vertices]

        # Scatter points
        self.canvas.scatter(xs, ys, s=50, color=Colors.VERTICES, zorder=10, **kwargs)

        return self

    def plot_outgoing_edges(self, vertices=None, scale=0.5, **kwargs):
        """
        Show arrows of length `scale` in the direction of the outgoing edges for each vertex.

        Parameters
        ----------
        vertices: list(:class:`voronoi.graph.Vertex`), optional
            The vertices for which to display the outgoing edges. By default, the `voronoi`'s vertices will be used.
        scale: float
            Used to set the length of the `outgoing_edges`.
        kwargs
            Optional arguments that are passed to arrowprops
        Returns
        -------
        self: Visualizer
        """
        vertices = vertices or self.voronoi.vertices
        scale = Decimal(str(scale))

        for vertex in vertices:
            for edge in vertex.connected_edges:
                start, end = self._origins(edge, None)

                if start is None or end is None:
                    continue

                # Direction vector
                x_diff = end.xd - start.xd
                y_diff = end.yd - start.yd
                length = Decimal.sqrt(x_diff ** 2 + y_diff ** 2)

                if length == 0:
                    continue

                direction = (x_diff / length, y_diff / length)
                new_end = Coordinate(start.xd + direction[0] * scale, start.yd + direction[1] * scale)

                props = dict(arrowstyle="->", color=Colors.EDGE_DIRECTION, linewidth=3, **kwargs)
                self.canvas.annotate(text='', xy=(new_end.xd, new_end.yd), xytext=(start.xd, start.yd),
                                     arrowprops=props)

        return self

    def plot_sites(self, points=None, show_labels=True, color=Colors.CELL_POINTS, zorder=10):
        """
        Display the cell points (a.k.a. sites).

        Parameters
        ----------
        points: list(:class:`voronoi.graph.Point`), optional
            The vertices to display. By default, the `voronoi`'s vertices will be used.
        show_labels: bool
            Display the labels of the cell points, of format "`P#`", where `#` is the `n`th point from top to bottom.
        color: str
            Color of the sites in hex format (e.g. "#bdc3c7").
        zorder: int
            Higher order will be shown on top of a lower layer.

        Returns
        -------
        self: Visualizer
        """
        points = points or self.voronoi.sites

        xs = [point.xd for point in points]
        ys = [point.yd for point in points]

        # Scatter points
        self.canvas.scatter(xs, ys, s=50, color=color, zorder=zorder)

        # Add descriptions
        if show_labels:
            for point in points:
                self.canvas.text(point.xd, point.yd, s=f"P{point.name if point.name is not None else ''}", zorder=15)

        return self

    def plot_edges(self, edges=None, sweep_line=None, show_labels=True, color=Colors.EDGE, **kwargs):
        """
        Display the borders of the cells.

        Parameters
        ----------
        edges: list(:class:`voronoi.graph.HalfEdge`), optional
            The edges to display. By default, the `voronoi`'s edges will be used.
        sweep_line: Decimal
            The y-coordinate of the sweep line, used to calculate the positions of unfinished edges. By default, the
            `voronoi`'s sweep_line will be used.
        show_labels: bool
            Display edge labels of format "`A/B`", where the edge is `A`'s border and the edge's twin is `B`'s border.
        color: str
            Color of the sites in hex format (e.g. "#636e72").

        Returns
        -------
        self: Visualizer
        """
        edges = edges or self.voronoi.edges
        sweep_line = sweep_line or self.voronoi.sweep_line
        for edge in edges:
            self._plot_edge(edge, sweep_line, show_labels, color)
            self._plot_edge(edge.twin, sweep_line, print_name=False, color=color)

        return self

    def plot_border_to_site(self, edges=None, sweep_line=None):
        """
        Indicate with dashed line to which site a border belongs. The site's first edge is colored green.

        Parameters
        ----------
        edges: list(:class:`voronoi.graph.HalfEdge`), optional
            The edges to display. By default, the `voronoi`'s edges will be used.
            
        sweep_line: Decimal
            The y-coordinate of the sweep line, used to calculate the positions of unfinished edges. By default, the
            `voronoi`'s sweep_line will be used.

        Returns
        -------
        self: Visualizer
        """
        edges = edges or self.voronoi.edges
        sweep_line = sweep_line or self.voronoi.sweep_line
        for edge in edges:
            self._draw_line_from_edge_midpoint_to_incident_point(edge, sweep_line)
            self._draw_line_from_edge_midpoint_to_incident_point(edge.twin, sweep_line)

        return self

    def plot_arcs(self, arcs=None, sweep_line=None, plot_arcs=False, show_labels=True):
        """
        Display each arc for each point. Only used if `beach_line` is also `True`.
        *Only useful during construction.*
        
        Parameters
        ----------
        arcs: list(:ref:`Arc`)
        sweep_line: Decimal
            The y-coordinate of the sweep line, used to calculate the positions of the arcs. By default, the
            `voronoi`'s sweep_line will be used.
        plot_arcs: bool
            Display each arc for each point
        show_labels: bool
            Display labels on the arcs.

        Returns
        -------
        self: Visualizer

        """
        arcs = arcs or self.voronoi.arcs
        sweep_line = sweep_line or self.voronoi.sweep_line

        # Get axis limits
        min_x, max_x, min_y, max_y = self.min_x, self.max_x, self.min_y, self.max_y
        sweep_line = max_y if sweep_line is None else sweep_line

        # Create 1000 equally spaced points
        x = np.linspace(float(min_x), float(max_x), 1000)

        plot_lines = []

        for arc in arcs:
            plot_line = arc.get_plot(x, sweep_line)

            if plot_line is None:
                if plot_arcs:
                    self.canvas.axvline(x=arc.origin.xd, color=Colors.SWEEP_LINE)
            else:
                if plot_arcs:
                    self.canvas.plot(x, plot_line, linestyle="--", color=Colors.ARC)

                plot_lines.append(plot_line)

        # Plot the bottom of all the arcs
        if len(plot_lines) > 0:
            bottom = np.min(plot_lines, axis=0)
            self.canvas.plot(x, bottom, color=Colors.BEACH_LINE)

            if show_labels:
                self._plot_arc_labels(x, plot_lines, bottom, sweep_line, arcs)

        return self

    def _plot_arc_labels(self, x, plot_lines, bottom, sweep_line, arcs):
        indices = np.nanargmin(plot_lines, axis=0)
        unique_indices = np.unique(indices)

        for index in unique_indices:
            x_mean = np.nanmedian(x[(indices == index) & (bottom < self.max_y)])
            y = arcs[index].get_plot(x_mean, sweep_line)
            self.canvas.text(x_mean, y, s=f"{arcs[index].origin.name}", size=12, color=Colors.VALID_CIRCLE, zorder=15)

        return self

    def plot_sweep_line(self, sweep_line=None):
        """
        Plot the sweep line.
        
        Parameters
        ----------
        sweep_line: Decimal
            The y-coordinate of the sweep line. By default, the `voronoi`'s sweep_line will be used.

        Returns
        -------
        self: Visualizer
        """
        sweep_line = sweep_line or self.voronoi.sweep_line

        # Get axis limits
        min_x, max_x, min_y, max_y = self.min_x, self.max_x, self.min_y, self.max_y

        self.canvas.plot([min_x, max_x], [sweep_line, sweep_line], color=Colors.SWEEP_LINE)

        return self

    def plot_event(self, event=None, triangles=False):
        """
        Display circles for circle events.
        *Only useful during construction.*

        Parameters
        ----------
        event: Event
            A circle event. Other events will be ignored.
        triangles: bool
            Display the triangle of the 3 points responsible for causing a circle event.

        Returns
        -------
        self: Visualizer
        """
        event = event or self.voronoi.event
        if isinstance(event, CircleEvent):
            self._plot_circle(event, show_triangle=triangles)

        return self

    def _plot_circle(self, evt, show_triangle=False):
        x, y = evt.center.xd, evt.center.yd
        radius = evt.radius
        color = Colors.VALID_CIRCLE if evt.is_valid else Colors.INVALID_CIRCLE

        circle = plt.Circle((x, y), radius, fill=False, color=color, linewidth=2)
        self.canvas.add_artist(circle)

        if show_triangle:
            triangle = plt.Polygon(evt.get_triangle(), fill=False, color=Colors.TRIANGLE, linewidth=1)
            self.canvas.add_artist(triangle)

        points = evt.point_triple
        self.plot_sites(points, color=Colors.VALID_CIRCLE, show_labels=False, zorder=15)

        return self

    def _plot_edge(self, edge, sweep_line=None, print_name=True, color=Colors.EDGE, **kwargs):

        start, end = self._origins(edge, sweep_line)

        # Return if conditions not met
        if not (start and end):
            return self

        # Draw the line
        self.canvas.plot([start.xd, end.xd], [start.yd, end.yd], color)

        # Add Name
        if print_name:
            self.canvas.annotate(
                text=str(edge),
                xy=((end.xd + start.xd) / 2, (end.yd + start.yd) / 2),
                **kwargs
            )

        # Add arrow
        # ax.annotate(text='', xy=(end.x, end.y), xytext=(start.x, start.y),
        #             arrowprops=dict(arrowstyle='->', **kwargs))

        return self

    def _draw_line_from_edge_midpoint_to_incident_point(self, edge, sweep_line=None):
        start, end = self._origins(edge, sweep_line)
        is_first_edge = edge.incident_point is not None and edge.incident_point.first_edge == edge
        incident_point = edge.incident_point
        if start and end and incident_point:
            self.canvas.plot(
                [(start.xd + end.xd) / 2, incident_point.xd], [(start.yd + end.yd) / 2, incident_point.yd],
                color=Colors.FIRST_EDGE if is_first_edge else Colors.INCIDENT_POINT_POINTER,
                linestyle="--"
            )
        return self.canvas

    def _origins(self, edge, sweep_line=None):

        # Get axis limits
        max_y = self.max_y

        # Get start and end of edges
        start = edge.get_origin(sweep_line, max_y)
        end = edge.twin.get_origin(sweep_line, max_y)

        return start, end

    @staticmethod
    def _canvas_size(bounding_polygon, offset):
        max_y = bounding_polygon.max_y + offset
        max_x = bounding_polygon.max_x + offset
        min_x = bounding_polygon.min_x - offset
        min_y = bounding_polygon.min_y - offset
        return min_x, max_x, min_y, max_y

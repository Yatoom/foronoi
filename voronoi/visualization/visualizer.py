from decimal import Decimal

import numpy as np
from matplotlib import patches

from voronoi import DecimalCoordinate
from voronoi.algorithm import Algorithm
from voronoi.events import CircleEvent
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


class Visualizer:

    def __init__(self, bounding_polygon, canvas_offset, figsize=(8, 8)):
        self.bounding_polygon = bounding_polygon
        self.min_x, self.max_x, self.min_y, self.max_y = self.canvas_size(bounding_polygon, canvas_offset)
        fig, ax = plt.subplots(figsize=figsize)
        self.canvas = ax

    def set_limits(self):
        self.canvas.set_ylim(self.min_y, self.max_y)
        self.canvas.set_xlim(self.min_x, self.max_x)
        return self

    def get_canvas(self):
        self.set_limits()
        return self.canvas.figure

    def show(self, block=True, **kwargs):
        self.set_limits()
        plt.show(block=block, **kwargs)
        return self

    def plot_all(self, voronoi: Algorithm, polygon=True, edges=True, vertices=True, sites=True,
                 outgoing_edges=False, events=True, beachline=True, arcs=True, border_to_site=False, scale=1,
                 show_edge_labels=True, show_point_labels=True, show_triangles=False, sweep_line=True):

        self.plot_sweep_line(sweep_line=voronoi.sweep_line) if sweep_line else False
        self.plot_polygon() if polygon else False
        self.plot_edges(voronoi.edges, sweep_line=voronoi.sweep_line, show_labels=show_edge_labels) if edges else False
        self.plot_border_to_site(voronoi.edges, sweep_line=voronoi.sweep_line) if border_to_site else False
        self.plot_vertices(voronoi.vertices) if vertices else False
        self.plot_sites(voronoi.points, show_labels=show_point_labels) if sites else False
        self.plot_outgoing_edges(voronoi.vertices, scale=scale) if outgoing_edges else False
        self.plot_events(voronoi.event_queue, show_triangles) if events else False
        self.plot_arcs(voronoi.arcs, sweep_line=voronoi.sweep_line, plot_arcs=arcs) if beachline else False
        self.set_limits()
        return self

    def plot_polygon(self):
        if hasattr(self.bounding_polygon, 'radius'):
            # Draw bounding box
            self.canvas.add_patch(
                patches.Circle((self.bounding_polygon.x, self.bounding_polygon.x), self.bounding_polygon.radius,
                               fill=False,
                               edgecolor=Colors.BOUNDING_BOX)
            )
        else:
            # Draw bounding box
            self.canvas.add_patch(
                patches.Polygon(self.bounding_polygon.get_coordinates(), fill=False, edgecolor=Colors.BOUNDING_BOX)
            )

        return self

    def plot_vertices(self, vertices, **kwargs):
        xs = [vertex.position.x for vertex in vertices]
        ys = [vertex.position.y for vertex in vertices]

        # Scatter points
        self.canvas.scatter(xs, ys, s=50, color=Colors.VERTICES, zorder=10, **kwargs)

        return self

    def plot_outgoing_edges(self, vertices, scale=1, **kwargs):
        for vertex in vertices:
            for edge in vertex.connected_edges:
                start, end = self._origins(edge, None)

                if start is None or end is None:
                    continue

                # Direction vector
                x_diff = end.x - start.x
                y_diff = end.y - start.y
                length = Decimal.sqrt(x_diff ** 2 + y_diff ** 2)

                if length == 0:
                    continue

                direction = (x_diff / length, y_diff / length)
                new_end = DecimalCoordinate(start.x + direction[0] * scale, start.y + direction[1] * scale)

                props = dict(arrowstyle="->", color=Colors.EDGE_DIRECTION, linewidth=1, **kwargs)
                self.canvas.annotate(text='', xy=(new_end.x, new_end.y), xytext=(start.x, start.y), arrowprops=props)

        return self

    def plot_sites(self, points, show_labels=True):
        xs = [point.x for point in points]
        ys = [point.y for point in points]

        # Scatter points
        self.canvas.scatter(xs, ys, s=50, color=Colors.CELL_POINTS, zorder=10)

        # Add descriptions
        if show_labels:
            for point in points:
                self.canvas.text(point.x, point.y, s=f"{point} (A={point.cell_size(digits=2)})", zorder=15)

        return self

    def plot_edges(self, edges, sweep_line=None, show_labels=True, color=Colors.EDGE, **kwargs):
        for edge in edges:
            self._plot_edge(edge, sweep_line, show_labels, color)
            self._plot_edge(edge.twin, sweep_line, print_name=False, color=color)

        return self

    def plot_border_to_site(self, edges, sweep_line=None):
        for edge in edges:
            self._draw_line_from_edge_midpoint_to_incident_point(edge, sweep_line)
            self._draw_line_from_edge_midpoint_to_incident_point(edge.twin, sweep_line)

        return self

    def plot_arcs(self, arcs, sweep_line=None, plot_arcs=True):

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
                    self.canvas.axvline(x=arc.origin.x, color=Colors.SWEEP_LINE)
            else:
                if plot_arcs:
                    self.canvas.plot(x, plot_line, linestyle="--", color=Colors.ARC)

                plot_lines.append(plot_line)

        # Plot the bottom of all the arcs
        if len(plot_lines) > 0:
            self.canvas.plot(x, np.min(plot_lines, axis=0), color=Colors.BEACH_LINE)

        return self

    def plot_sweep_line(self, sweep_line):

        # Get axis limits
        min_x, max_x, min_y, max_y = self.min_x, self.max_x, self.min_y, self.max_y

        self.canvas.plot([min_x, max_x], [sweep_line, sweep_line], color=Colors.SWEEP_LINE)

        return self

    def plot_events(self, event_queue, show_triangles=False):
        for event in event_queue.queue:
            if isinstance(event, CircleEvent):
                self._plot_circle(event, show_triangle=show_triangles)

        return self

    def _plot_circle(self, evt, show_triangle=False):
        x, y = evt.center.x, evt.center.y
        radius = evt.radius
        color = Colors.VALID_CIRCLE if evt.is_valid else Colors.INVALID_CIRCLE

        circle = plt.Circle((x, y), radius, fill=False, color=color, linewidth=2)
        self.canvas.add_artist(circle)

        if show_triangle:
            triangle = plt.Polygon(evt.get_triangle(), fill=False, color=Colors.TRIANGLE, linewidth=1)
            self.canvas.add_artist(triangle)

        return self


    def _plot_edge(self, edge, sweep_line=None, print_name=True, color=Colors.EDGE, **kwargs):

        start, end = self._origins(edge, sweep_line)

        # Return if conditions not met
        if not (start and end):
            return self

        # Draw the line
        self.canvas.plot([start.x, end.x], [start.y, end.y], color)

        # Add Name
        if print_name:
            self.canvas.annotate(
                text=str(edge),
                xy=((end.x + start.x) / 2, (end.y + start.y) / 2),
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
                [(start.x + end.x) / 2, incident_point.x], [(start.y + end.y) / 2, incident_point.y],
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
        start, end = self._cut_line(start, end)

        return start, end

    def _cut_line(self, start, end):

        min_x, max_x, min_y, max_y = self.min_x, self.max_x, self.min_y, self.max_y

        if start is not None:
            start.x = max(min_x, min(max_x, start.x))
            start.y = max(min_y, min(max_y, start.y))

        if end is not None:
            end.x = max(min_x, min(max_x, end.x))
            end.y = max(min_y, min(max_y, end.y))

        return start, end

    @staticmethod
    def canvas_size(bounding_polygon, offset):
        max_y = bounding_polygon.max_y + offset
        max_x = bounding_polygon.max_x + offset
        min_x = bounding_polygon.min_x - offset
        min_y = bounding_polygon.min_y - offset
        return min_x, max_x, min_y, max_y

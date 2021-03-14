from decimal import Decimal

import numpy as np
from matplotlib import patches

from voronoi import DecimalCoordinate
from voronoi.algorithm import Algorithm
from voronoi.events import CircleEvent
import matplotlib.pyplot as plt


class Colors:
    SWEEP_LINE = "#16a085"
    VERTICES = "#e67e22"
    BEACH_LINE = "#636e72"
    EDGE = "#636e72"
    ARC = "#b2bec3"
    INCIDENT_POINT_POINTER = "#dfe6e9"
    INVALID_CIRCLE = "#e74c3c"  # red
    VALID_CIRCLE = "#3498db"  # blue
    CELL_POINTS = "#34495e"  # blue
    TRIANGLE = "#00cec9"  # orange
    BOUNDING_BOX = "black"  # blue
    TEXT = "#00cec9"  # green
    HELPER = "#ff0000"
    HIGH_LIGHT = "#00ff00"
    EDGE_DIRECTION = "#fdcb6e"
    FIRST_EDGE = "#2ecc71"


class Visualizer:

    def __init__(self, bounding_polygon, canvas_offset):
        self.bounding_polygon = bounding_polygon
        self.min_x, self.max_x, self.min_y, self.max_y = self.canvas_size(bounding_polygon, canvas_offset)

    def set_limits(self, ax):
        ax.set_ylim(self.min_y, self.max_y)
        ax.set_xlim(self.min_x, self.max_x)
        return ax

    def plot_all(self, ax, voronoi: Algorithm, polygon=True, edges=True, vertices=True, sites=True,
                 outgoing_edges=False, events=True, beachline=True, arcs=True, scale=1):

        ax = self.plot_sweep_line(ax, sweep_line=voronoi.sweep_line)
        ax = self.plot_polygon(ax) if polygon else ax
        ax = self.plot_edges(ax, voronoi.edges, sweep_line=voronoi.sweep_line) if edges else ax
        ax = self.plot_vertices(ax, voronoi.vertices) if vertices else ax
        ax = self.plot_sites(ax, voronoi.points) if sites else ax
        ax = self.plot_outgoing_edges(ax, voronoi.vertices, scale=scale) if outgoing_edges else ax
        ax = self.plot_events(ax, voronoi.event_queue) if events else ax
        ax = self.plot_arcs(ax, voronoi.arcs, sweep_line=voronoi.sweep_line, plot_arcs=arcs) if beachline else ax
        return ax

    def plot_polygon(self, ax):
        if hasattr(self.bounding_polygon, 'radius'):
            # Draw bounding box
            ax.add_patch(
                patches.Circle((self.bounding_polygon.x, self.bounding_polygon.x), self.bounding_polygon.radius,
                               fill=False,
                               edgecolor=Colors.BOUNDING_BOX)
            )
        else:
            # Draw bounding box
            ax.add_patch(
                patches.Polygon(self.bounding_polygon.get_coordinates(), fill=False, edgecolor=Colors.BOUNDING_BOX)
            )

        return self.set_limits(ax)

    def plot_vertices(self, ax, vertices, **kwargs):
        xs = [vertex.position.x for vertex in vertices]
        ys = [vertex.position.y for vertex in vertices]

        # Scatter points
        ax.scatter(xs, ys, s=50, color=Colors.VERTICES, **kwargs)

        return self.set_limits(ax)

    def plot_outgoing_edges(self, ax, vertices, scale=1, **kwargs):
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

                props = dict(arrowstyle="->", color=Colors.EDGE_DIRECTION, linewidth=2, **kwargs)
                ax.annotate(text='', xy=(new_end.x, new_end.y), xytext=(start.x, start.y), arrowprops=props)

        return self.set_limits(ax)

    def plot_sites(self, ax, points):
        xs = [point.x for point in points]
        ys = [point.y for point in points]

        # Scatter points
        ax.scatter(xs, ys, s=50, color=Colors.CELL_POINTS)

        # Add descriptions
        for point in points:
            ax.text(point.x, point.y, s=f"{point} ({point.cell_size(digits=2)})")

        return ax

    def plot_edges(self, ax, edges, sweep_line=None, print_name=True, color=Colors.EDGE, indicate_incident=True,
                   **kwargs):
        for edge in edges:
            ax = self._plot_edge(ax, edge, sweep_line, print_name, color)
            if indicate_incident:
                ax = self._draw_line_from_edge_midpoint_to_incident_point(ax, edge, sweep_line)

        return self.set_limits(ax)

    def plot_arcs(self, ax, arcs, sweep_line=None, plot_arcs=True):

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
                    ax.axvline(x=arc.origin.x, color=Colors.SWEEP_LINE)
            else:
                if plot_arcs:
                    ax.plot(x, plot_line, linestyle="--", color=Colors.ARC)

                plot_lines.append(plot_line)

        # Plot the bottom of all the arcs
        if len(plot_lines) > 0:
            ax.plot(x, np.min(plot_lines, axis=0), color=Colors.BEACH_LINE)

        return self.set_limits(ax)

    def plot_sweep_line(self, ax, sweep_line):

        # Get axis limits
        min_x, max_x, min_y, max_y = self.min_x, self.max_x, self.min_y, self.max_y

        ax.plot([min_x, max_x], [sweep_line, sweep_line], color=Colors.SWEEP_LINE)

        return self.set_limits(ax)

    def plot_events(self, ax, event_queue):
        for event in event_queue.queue:
            if isinstance(event, CircleEvent):
                self._plot_circle(ax, event)

        return self.set_limits(ax)

    def _plot_circle(self, ax, evt):
        x, y = evt.center.x, evt.center.y
        radius = evt.radius
        color = Colors.VALID_CIRCLE if evt.is_valid else Colors.INVALID_CIRCLE

        circle = plt.Circle((x, y), radius, fill=False, color=color, linewidth=1.2)
        triangle = plt.Polygon(evt.get_triangle(), fill=False, color=Colors.TRIANGLE, linewidth=1.2)

        ax.add_artist(circle)
        ax.add_artist(triangle)

        return self.set_limits(ax)

    def _plot_edge(self, ax, edge, sweep_line=None, print_name=True, color=Colors.EDGE, **kwargs):

        start, end = self._origins(edge, sweep_line)

        # Return if conditions not met
        if not (start and end):
            return ax

        # Draw the line
        ax.plot([start.x, end.x], [start.y, end.y], color)

        # Add Name
        if print_name:
            ax.annotate(
                text=str(edge),
                xy=((end.x + start.x) / 2, (end.y + start.y) / 2),
                **kwargs
            )

        # Add arrow
        # ax.annotate(text='', xy=(end.x, end.y), xytext=(start.x, start.y),
        #             arrowprops=dict(arrowstyle='->', **kwargs))

        return self.set_limits(ax)

    def _draw_line_from_edge_midpoint_to_incident_point(self, ax, edge, sweep_line=None):
        start, end = self._origins(edge, sweep_line)
        is_first_edge = edge.incident_point is not None and edge.incident_point.first_edge == edge
        incident_point = edge.incident_point
        if start and end and incident_point:
            ax.plot(
                [(start.x + end.x) / 2, incident_point.x], [(start.y + end.y) / 2, incident_point.y],
                color=Colors.FIRST_EDGE if is_first_edge else Colors.INCIDENT_POINT_POINTER,
                linestyle="--"
            )
        return ax

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

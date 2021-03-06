import time

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from voronoi.events import CircleEvent


class Colors:
    SWEEP_LINE = "#636e72"
    CELL_POINTS = "black"
    BEACH_LINE = "#636e72"
    EDGE = "#636e72"
    ARC = "#b2bec3"
    INCIDENT_POINT_POINTER = "#FDAB81"
    INCIDENT_POINT_POINTER_TWIN = "#dfe6e9"
    INVALID_CIRCLE = "#d63031"  # red
    VALID_CIRCLE = "#0984e3"  # blue
    VERTICES = "#0984e3"  # blue
    TRIANGLE = "#00cec9"  # orange
    BOUNDING_BOX = "black"  # blue
    TEXT = "#00cec9"  # green
    HELPER = "#ff0000"
    HIGH_LIGHT = "#00ff00"


class Visualization(object):

    def visualize(self, y, current_event, bounding_poly, points, vertices, edges, arc_list, event_queue,
                  calc_cell_sizes=True):
        self.fig, self.ax = plt.subplots(figsize=(17, 17))
        self.ax.set_title(str(current_event))
        scale = (bounding_poly.max_y - bounding_poly.min_y)
        border = (bounding_poly.max_y - bounding_poly.min_y) / 4
        plt.ylim((bounding_poly.min_y - border, bounding_poly.max_y + border))
        plt.xlim((bounding_poly.min_x - border, bounding_poly.max_x + border))

        # Create 1000 equally spaced points between -10 and 10 and setup plot window
        x = np.linspace(float(bounding_poly.min_x), float(bounding_poly.max_x), 1000)
        x_full = np.linspace(float(bounding_poly.min_x) - float(border), float(bounding_poly.max_x + border), 1000)

        # Plot the sweep line
        self.ax.plot([bounding_poly.min_x - border, bounding_poly.max_x + border], [y, y], color=Colors.SWEEP_LINE)

        # Plot all arcs
        plot_lines = []
        for arc in arc_list:
            plot_line = arc.get_plot(x_full, y)
            if plot_line is None:
                self.ax.axvline(x=arc.origin.x)
            else:
                self.ax.plot(x_full, plot_line, linestyle="--", color=Colors.ARC)
                plot_lines.append(plot_line)

        # Plot the beach line, i.e. the bottom of all the arcs
        if len(plot_lines) > 0:
            self.ax.plot(x_full, np.min(plot_lines, axis=0), color=Colors.BEACH_LINE)

        # Plot half-edges
        for edge in edges:
            self._plot_edge(edge, y, bounding_poly)

        if isinstance(current_event, CircleEvent):
            self._plot_circle(current_event, self.ax)

        for event in event_queue.queue:
            if isinstance(event, CircleEvent):
                self._plot_circle(event, self.ax)

        if hasattr(bounding_poly, 'radius'):
            # Draw bounding box
            self.ax.add_patch(
                patches.Circle((bounding_poly.x, bounding_poly.x), bounding_poly.radius, fill=False,
                               edgecolor=Colors.BOUNDING_BOX)
            )
        else:
            # Draw bounding box
            self.ax.add_patch(
                patches.Polygon(bounding_poly.get_coordinates(), fill=False, edgecolor=Colors.BOUNDING_BOX)
            )

        # Plot vertices
        for vertex in vertices:
            x, y = vertex.position.x, vertex.position.y
            self.ax.scatter(x=[x], y=[y], s=50, color=Colors.VERTICES)

        # Plot points
        for point in points:
            x, y = point.x, point.y
            self.ax.scatter(x=[x], y=[y], s=50, color=Colors.CELL_POINTS)
            text = str(point)

            if calc_cell_sizes:
                text += " " + str(point.cell_size(digits=2))

            self.ax.text(s=text, x=x + scale / 100, y=y + scale / 100, color=Colors.TEXT)

        plt.show(block=True)

    # Plot circle events
    @staticmethod
    def _plot_circle(evt, ax):
        x, y = evt.center.x, evt.center.y
        radius = evt.radius
        color = Colors.VALID_CIRCLE if evt.is_valid else Colors.INVALID_CIRCLE

        # if evt.is_valid:
        circle = plt.Circle((x, y), radius, fill=False, color=color, linewidth=1.2)
        triangle = plt.Polygon(evt.get_triangle(), fill=False, color=Colors.TRIANGLE, linewidth=1.2)
        ax.add_artist(circle)
        ax.add_artist(triangle)

    def plot_helper_points(self, A, B, center, start_ray, a, b, c):
        self.ax.scatter(x=[A.x, B.x, center.x, start_ray.x], y=[A.y, B.y, center.y, start_ray.y], s=50,
                        color=Colors.HELPER)
        self.ax.plot(
            [start_ray.x, center.x], [start_ray.y, (c - a * center.x) / b],
            color=Colors.HELPER
        )
        self.fig.show()

    def plot_points(self, A, B):
        self.ax.scatter(x=[A.x, B.x], y=[A.y, B.y], s=50, color=Colors.HELPER)
        self.fig.show()

    def highlight_edge(self, y, bounding_poly, edge):
        # Get start and end of edges
        start = edge.get_origin(y, bounding_poly.max_y)
        end = edge.twin.get_origin(y, bounding_poly.max_y)

        # Draw line
        if start and end:
            self.ax.plot([start.x, end.x], [start.y, end.y], Colors.HIGH_LIGHT, linewidth=5)

        # Add arrow
        if start and end and start.y < float('inf'):
            self.ax.annotate(
                s='',
                xy=(end.x, end.y),
                xytext=(start.x, start.y),
                arrowprops=dict(
                    arrowstyle='->',
                    linewidth=5,
                    color=Colors.HIGH_LIGHT
                )
            )

        self.fig.show()

    def _plot_edge(self, edge, y, bounding_poly):
        # Get start and end of edges
        start = edge.get_origin(y, bounding_poly.max_y)
        end = edge.twin.get_origin(y, bounding_poly.max_y)

        # Draw line
        if start and end:
            self.ax.plot([start.x, end.x], [start.y, end.y], Colors.EDGE)
            # Add Name
            plt.annotate(
                text=str(edge),
                xy=((end.x + start.x) / 2, (end.y + start.y) / 2)
            )

        # Add arrow
        if start and end and start.y < float('inf'):
            plt.annotate(text='', xy=(end.x, end.y), xytext=(start.x, start.y), arrowprops=dict(arrowstyle='->'))

        # Point to incident point
        self.draw_pointer_to_incident_point(edge, start, end, Colors.INCIDENT_POINT_POINTER)
        self.draw_pointer_to_incident_point(edge.twin, end, start, Colors.INCIDENT_POINT_POINTER_TWIN)

    def draw_pointer_to_incident_point(self, edge, start, end, color):
        incident_point = edge.incident_point
        if start and end and incident_point:
            self.ax.plot(
                [(start.x + end.x) / 2, incident_point.x], [(start.y + end.y) / 2, incident_point.y],
                color=color,
                linestyle="--"
            )
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
    INCIDENT_POINT_POINTER = "#dfe6e9"
    INVALID_CIRCLE = "#d63031"  # red
    VALID_CIRCLE = "#0984e3"  # blue
    VERTICES = "#0984e3"  # blue
    TRIANGLE = "#00cec9"  # orange
    BOUNDING_BOX = "black"  # blue
    TEXT = "#00cec9"  # green


def visualize(y, current_event, bounding_poly, points, vertices, edges, arc_list, event_queue, calc_cell_sizes=True):
    fig, ax = plt.subplots(figsize=(7, 7))
    plt.title(current_event)
    scale = (bounding_poly.max_y - bounding_poly.min_y)
    border = (bounding_poly.max_y - bounding_poly.min_y) / 4
    plt.ylim((bounding_poly.min_y - border, bounding_poly.max_y + border))
    plt.xlim((bounding_poly.min_x - border, bounding_poly.max_x + border))

    # Create 1000 equally spaced points between -10 and 10 and setup plot window
    x = np.linspace(bounding_poly.min_x, bounding_poly.max_x, 1000)
    x_full = np.linspace(bounding_poly.min_x - border, bounding_poly.max_x + border, 1000)

    # Plot the sweep line
    ax.plot([bounding_poly.min_x - border, bounding_poly.max_x + border], [y, y], color=Colors.SWEEP_LINE)

    # Plot all arcs
    plot_lines = []
    for arc in arc_list:
        plot_line = arc.get_plot(x_full, y)
        if plot_line is None:
            ax.axvline(x=arc.origin.x)
        else:
            ax.plot(x_full, plot_line, linestyle="--", color=Colors.ARC)
            plot_lines.append(plot_line)
    if len(plot_lines) > 0:
        ax.plot(x_full, np.min(plot_lines, axis=0), color=Colors.BEACH_LINE)

    # Plot circle events
    def plot_circle(evt):
        x, y = evt.center.x, evt.center.y
        radius = evt.radius
        color = Colors.VALID_CIRCLE if evt.is_valid else Colors.INVALID_CIRCLE

        # if evt.is_valid:
        circle = plt.Circle((x, y), radius, fill=False, color=color, linewidth=1.2)
        triangle = plt.Polygon(evt.get_triangle(), fill=False, color=Colors.TRIANGLE, linewidth=1.2)
        ax.add_artist(circle)
        ax.add_artist(triangle)

    # Plot half-edges
    for edge in edges:

        # Get start and end of edges
        start = edge.get_origin(y, bounding_poly.max_y)
        end = edge.twin.get_origin(y, bounding_poly.max_y)

        # Draw line
        if start and end:
            plt.plot([start.x, end.x], [start.y, end.y], Colors.EDGE)

        # Add arrow
        if start and end and start.y < float('inf'):
            plt.annotate(s='', xy=(end.x, end.y), xytext=(start.x, start.y), arrowprops=dict(arrowstyle='->'))

        # Point to incident point
        incident_point = edge.incident_point
        if start and end and incident_point:
            plt.plot(
                [(start.x + end.x) / 2, incident_point.x], [(start.y + end.y) / 2, incident_point.y],
                color=Colors.INCIDENT_POINT_POINTER,
                linestyle="--"
            )

    if isinstance(current_event, CircleEvent):
        plot_circle(current_event)

    for event in event_queue.queue:
        if isinstance(event, CircleEvent):
            plot_circle(event)

    # Draw bounding box
    ax.add_patch(
        patches.Polygon(bounding_poly.get_coordinates(), fill=False, edgecolor=Colors.BOUNDING_BOX)
    )

    # Plot vertices
    for vertex in vertices:
        x, y = vertex.position.x, vertex.position.y
        ax.scatter(x=[x], y=[y], s=50, color=Colors.VERTICES)

    # Plot points
    for point in points:
        x, y = point.x, point.y
        ax.scatter(x=[x], y=[y], s=50, color=Colors.CELL_POINTS)

        if calc_cell_sizes:
            size = f"{point.cell_size(digits=2)}"
            # plt.annotate(s=size, xy=(x, y), xytext=(100, y), arrowprops=dict(arrowstyle='->', facecolor="white"))
            plt.text(s=size, x=x + scale / 100, y=y + scale / 100, color=Colors.TEXT)

    plt.show()

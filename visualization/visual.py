import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from events import CircleEvent


def visualize(y, current_event, bounding_box, points, vertices, edges, arc_list, event_queue):
    # Create 1000 equally spaced points between -10 and 10 and setup plot window
    x = np.linspace(bounding_box.left, bounding_box.right, 1000)
    fig, ax = plt.subplots(figsize=(7, 7))
    plt.title(current_event)
    plt.ylim((bounding_box.bottom - 1, bounding_box.top + 1))
    plt.xlim((bounding_box.left - 1, bounding_box.right + 1))

    # Plot the sweep line
    ax.plot(x, x + y - x, color='black')

    # Plot all arcs
    plot_lines = []
    for arc in arc_list:
        plot_line = arc.get_plot(x, y)
        if plot_line is None:
            ax.axvline(x=arc.origin.x)
        else:
            ax.plot(x, plot_line, linestyle="--", color='gray')
            plot_lines.append(plot_line)
    if len(plot_lines) > 0:
        ax.plot(x, np.min(plot_lines, axis=0), color="black")

    # Plot circle events
    def plot_circle(evt):
        x, y = evt.center.x, evt.center.y
        radius = evt.radius
        color = "#1f77b4" if evt.is_valid else "#f44336"

        # if evt.is_valid:
        circle = plt.Circle((x, y), radius, fill=False, color=color, linewidth=1.2)
        triangle = plt.Polygon(evt.get_triangle(), fill=False, color="#ff7f0e", linewidth=1.2)
        ax.add_artist(circle)
        ax.add_artist(triangle)

    # Plot half-edges
    for edge in edges:

        # Get start and end of edges
        start = edge.get_origin(y, bounding_box)
        end = edge.twin.get_origin(y, bounding_box)

        # Draw line
        plt.plot([start.x, end.x], [start.y, end.y], color="black")

        # Add arrow
        if start.y < float('inf'):
            plt.annotate(s='', xy=(end.x, end.y), xytext=(start.x, start.y), arrowprops=dict(arrowstyle='->'))

        # Point to incident point
        incident_point = edge.incident_point
        if incident_point is not None:
            plt.plot(
                [(start.x + end.x) / 2, incident_point.x], [(start.y + end.y) / 2, incident_point.y],
                color="lightgray",
                linestyle="--"
            )

    if isinstance(current_event, CircleEvent):
        plot_circle(current_event)

    for event in event_queue.queue:
        if isinstance(event, CircleEvent):
            plot_circle(event)

    # Draw bounding box
    ax.add_patch(
        patches.Rectangle(
            (bounding_box.left, bounding_box.bottom),  # (x,y)
            bounding_box.right - bounding_box.left,  # width
            bounding_box.top - bounding_box.bottom,  # height
            fill=False
        )
    )

    # Plot vertices
    for vertex in vertices:
        x, y = vertex.position.x, vertex.position.y
        ax.scatter(x=[x], y=[y], s=50, color="blue")

    # Plot points
    for point in points:
        x, y = point.x, point.y
        ax.scatter(x=[x], y=[y], s=50, color="black")
        size = f"{point.cell_size(digits=2)}"
        # ax.text(x-0.5, y+1, size)
        plt.annotate(s=size, xy=(x, y), xytext=(x, y + 1), arrowprops=dict(arrowstyle='->'))

    plt.show()

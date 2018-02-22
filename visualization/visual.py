import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from events import CircleEvent


def visualize(self, y, current_event):
    # Create 1000 equally spaced points between -10 and 10 and setup plot window
    x = np.linspace(-25, 25, 1000)
    fig, ax = plt.subplots(figsize=(7, 7))
    plt.title(current_event)
    plt.ylim((self.bounding_box.bottom - 1, self.bounding_box.top + 1))
    plt.xlim((self.bounding_box.left - 1, self.bounding_box.right + 1))

    # Plot the sweep line
    ax.plot(x, x + y - x, color='black')

    # Plot all arcs
    plot_lines = []
    for arc in self.arc_list:
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
    for edge in self.edges:

        # Get start and end of edges
        start = edge.get_origin(y, self.bounding_box)
        end = edge.twin.get_origin(y, self.bounding_box)

        # Draw line
        plt.plot([start.x, end.x], [start.y, end.y], color="black")

        # Add arrow
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

    for event in self.event_queue.queue:
        if isinstance(event, CircleEvent):
            plot_circle(event)

    # Draw bounding box
    ax.add_patch(
        patches.Rectangle(
            (self.bounding_box.left, self.bounding_box.bottom),  # (x,y)
            self.bounding_box.right - self.bounding_box.left,  # width
            self.bounding_box.top - self.bounding_box.bottom,  # height
            fill=False
        )
    )

    # Plot vertices
    for vertex in self.vertices:
        x, y = vertex.position.x, vertex.position.y
        ax.scatter(x=[x], y=[y], s=50, color="blue")

    # Plot points
    for point in self.points:
        x, y = point.x, point.y
        ax.scatter(x=[x], y=[y], s=50, color="black")
        size = f"{point.cell_size(digits=2)}"
        # ax.text(x-0.5, y+1, size)
        plt.annotate(s=size, xy=(x, y), xytext=(x, y + 1), arrowprops=dict(arrowstyle='->'))

    plt.show()

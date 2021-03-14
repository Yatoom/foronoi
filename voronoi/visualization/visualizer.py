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
    HELPER = "#ff0000"
    HIGH_LIGHT = "#00ff00"
    EDGE_DIRECTION = "#fdcb6e"


class Visualizer:
    @staticmethod
    def plot_vertices(ax, vertices, **kwargs):
        xs = [vertex.position.x for vertex in vertices]
        ys = [vertex.position.y for vertex in vertices]

        # Scatter points
        ax.scatter(xs, ys, s=50, color=Colors.VERTICES, **kwargs)

        return ax

    @staticmethod
    def plot_sites(ax, points):
        xs = [point.x for point in points]
        ys = [point.y for point in points]

        # Scatter points
        ax.scatter(xs, ys, s=50, color=Colors.CELL_POINTS)

        # Add descriptions
        for point in points:
            ax.text(f"{point} ({point.cell_size(digits=2)})")

        return ax

    @staticmethod
    def plot_edges(ax, edges, sweep_line=None, print_name=True, color=Colors.EDGE, indicate_incident=True, **kwargs):
        for edge in edges:
            ax = Visualizer._plot_edge(ax, edge, sweep_line, print_name, color)
            if indicate_incident:
                ax = Visualizer._draw_line_from_edge_midpoint_to_incident_point(ax, edge, sweep_line)
        return ax

    @staticmethod
    def plot_arcs(ax, arcs, sweep_line=None, plot_arcs=True):

        # Get axis limits
        min_x, max_x = ax.get_xlim()
        min_y, max_y = ax.get_ylim()
        sweep_line = max_y if sweep_line is None else sweep_line

        # Create 1000 equally spaced points
        x = np.linspace(min_x, max_x, 1000)

        plot_lines = []

        for arc in arcs:
            plot_line = arc.get_plot(min_x, sweep_line)

            if plot_line is None:
                if plot_arcs:
                    ax.axvline(x=arc.origin.x)
            else:
                if plot_arcs:
                    ax.plot(x, plot_line, linestyle="--", color=Colors.ARC)

                plot_lines.append(plot_line)

        # Plot the bottom of all the arcs
        if len(plot_lines) > 0:
            ax.plot(x, np.min(plot_lines, axis=0), color=Colors.BEACH_LINE)

        return ax

    @staticmethod
    def plot_sweep_line(ax, sweep_line):

        # Get axis limits
        min_x, max_x = ax.get_xlim()
        min_y, max_y = ax.get_ylim()

        ax.plot([min_x, max_x], [sweep_line, sweep_line], color=Colors.SWEEP_LINE)

        return ax

    @staticmethod
    def plot_events(ax, event_queue):
        for event in event_queue.queue:
            if isinstance(event, CircleEvent):
                Visualizer._plot_circle(ax, event)

    @staticmethod
    def _plot_circle(ax, evt):
        x, y = evt.center.x, evt.center.y
        radius = evt.radius
        color = Colors.VALID_CIRCLE if evt.is_valid else Colors.INVALID_CIRCLE

        circle = ax.Circle((x, y), radius, fill=False, color=color, linewidth=1.2)
        triangle = ax.Polygon(evt.get_triangle(), fill=False, color=Colors.TRIANGLE, linewidth=1.2)
        ax.add_artist(circle)
        ax.add_artist(triangle)

        return ax


    @staticmethod
    def _plot_edge(ax, edge, sweep_line=None, print_name=True, color=Colors.EDGE, **kwargs):

        start, end = Visualizer._origins(ax, edge, sweep_line)

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

        return ax

    @staticmethod
    def _draw_line_from_edge_midpoint_to_incident_point(ax, edge, sweep_line=None):
        start, end = Visualizer._origins(ax, edge, sweep_line)
        is_first_edge = edge.incident_point is not None and edge.incident_point.first_edge == edge
        incident_point = edge.incident_point
        if start and end and incident_point:
            ax.plot(
                [(start.x + end.x) / 2, incident_point.x], [(start.y + end.y) / 2, incident_point.y],
                color="green" if is_first_edge else Colors.INCIDENT_POINT_POINTER,
                linestyle="--"
            )
        return ax

    @staticmethod
    def _origins(ax, edge, sweep_line=None):

        # Get axis limits
        min_y, max_y = ax.get_ylim()

        # Get start and end of edges
        start = edge.get_origin(sweep_line, max_y)
        end = edge.twin.get_origin(sweep_line, max_y)
        start, end = Visualizer._cut_line(ax, start, end)

        return start, end

    @staticmethod
    def _cut_line(ax, start, end):
        min_x, max_x = ax.get_xlim()
        min_y, max_y = ax.get_ylim()
        start.x = max(min_x, min(max_x, start.x))
        start.y = max(min_y, min(max_y, start.y))
        end.x = max(min_x, min(max_x, end.x))
        end.y = max(min_y, min(max_y, end.y))
        return start, end

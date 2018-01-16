import math
from typing import Union

from data_structures.bin_search_tree import AVLTree, Node


class GameState:
    """
    The current state of the game.
    It will hold the settings of the gameboard and a list of place points
    """
    points = []

    def __init__(self, width: int = 100, height: int = 100, m: int = None, n: int = None):
        self.width = width
        self.height = height
        self.m = m
        self.n = n


class Point:
    """
    A simple point
    """
    def __init__(self, x=None, y=None, player: int = None):
        self.x = x
        self.y = y
        self.player = player


class CirclePoint(Point):
    """
    A point that represents the lowest point of a circle.
    It has a pointer to the leaf in the beach line that represents the arc that will disappear in the event.
    """
    def __init__(self, pointer=None):
        super().__init__()
        self.pointer = pointer


class Breakpoint:
    """
    A breakpoint between two arcs.
    The internal nodes represent the breakpoints on the beach line.
    """

    def __init__(self, breakpoint=(None, None), pointer=None):
        """
        The breakpoint is stored by an ordered tuple of sites (p_i, p_j) where p_i defines the parabola left of the
        breakpoint and p_j defines the parabola to the right. Furthermore, the internal node v has a pointer to the half
        edge in the doubly connected edge list of the Voronoi diagram. More precisely, v has a pointer to one of the
        half-edges of the edge being traced out by the breakpoint represented by v.
        """
        self.breakpoint: tuple = breakpoint
        self.pointer = pointer

    def get_intersection(self, l):
        """
        Calculate the coordinates of the intersection
        Modified from https://www.cs.hmc.edu/~mbrubeck/voronoi.html

        :param l: (float) The position (y-coordinate) of the sweep line
        :return: (float) The coordinates of the breakpoint
        """

        # Get the points
        i, j = self.breakpoint

        # Initialize the resulting point
        result = Point()
        p: Point = i

        # Handle the case where the two points have the same y-coordinate (breakpoint is in the middle)
        if i.y == j.y:
            result.x = (i.x + j.x) / 2

        # Handle cases where one point's y-coordinate is the same as the sweep line
        elif i.y == l:
            result.x = i.x
            p = j
        elif j.y == l:
            result.x = j.x
        else:

            # Use quadratic formula to solve the problem
            z0 = 2 * (i.y - l)
            z1 = 2 * (i.y - l)

            a = 1 / z0 - 1 / z1
            b = -2 * (i.x / z0 - j.x / z1)
            c = (i.x ** 2 + i.y ** 2 - l ** 2) / z0 - (j.x ** 2 + j.y ** 2 - l ** 2) / z1

            result.x = (-b - math.sqrt(b ** 2 - 4 * a * c) / (2 * a))

        # Calculate the y-coordinate from the x coordinate
        result.y = (p.y ** 2 + (p.x - result.x) ** 2 - l ** 2) / (2 * p.y - 2 * l)

        return result


class Arc(Point):
    """
    Each leaf of beach line, representing an arc α, stores one pointer to a node in the event queue, namely, the node
    that represents the circle event in which α will disappear. This pointer is None if no circle event exists where α
    will disappear, or this circle event has not been detected yet.
    """
    pointer = None


class BeachLine(AVLTree):
    def find_arc_above_point(self, point, sweep_line):
        """
        Find an arc in the beach line.

        :param point: (Node) The root node of the subtree
        :param sweep_line: (float) The y-position of the sweep line
        :return: (Node or None) The found node, or None if there was no result
        """
        return self.find_arc_in_subtree(root=self.root, key=point.x, sweep_line=sweep_line)

    def replace_leaf(self, key, replacement_tree):
        node = self.root
        while node is not None:
            if node.left is not None and node.left.key == node.key:
                node.left = replacement_tree
                break
            elif node.right is not None and node.right.key == node.key:
                node.right = replacement_tree
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Return node, None if not found
        return node

    @staticmethod
    def find_arc_in_subtree(root: Union[Node, None], key: int, sweep_line: int) -> Node:
        """
        Find a node using binary search on a given key, within a subtree.

        :param root: (Node) The root node of the subtree
        :param key: (int) The key to search for
        :param sweep_line: (float) The y-position of the sweep line
        :return: (Node or None) The found node, or None if there was no result
        """

        node = root
        while node is not None:

            # Calculate x-coordinate of breakpoint
            node_key = node.key
            if isinstance(node.value, Breakpoint):
                node_key = node.value.get_intersection(sweep_line)

            # Found the arc
            if node.left is None and node.right is None:
                return node

            # Keep searching
            if key == node_key:
                break
            elif key < node_key:
                node = node.left
            else:
                node = node.right

        # Return node, None if not found
        return node

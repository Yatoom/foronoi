class Node:
    def __init__(self, data):
        """
        A smart tree node with some extra functionality over standard nodes.
        :param data: Data that is stored inside the node.
        """
        self.data = data
        self._left = None
        self._right = None
        self._height = None
        self.parent = None

    def __repr__(self):
        return f"Node({self.data}, left={self.left}, right={self.right})"

    @property
    def left(self) -> "Node":
        return self._left

    @property
    def right(self) -> "Node":
        return self._right

    @property
    def grandparent(self):
        if self.parent is None or self.parent.parent is None:
            return None
        return self.parent.parent

    def get_key(self, **kwargs):
        return self.data

    def get_value(self, **kwargs):
        return self.data

    def get_label(self, **kwargs):
        return f"{self.get_key(**kwargs)}({self.height})"

    @left.setter
    def left(self, node):

        if node is not None:

            # Tell the child who its new parent is
            node.parent = self

        self._left = node

    @right.setter
    def right(self, node):

        if node is not None:

            # Tell the child who its new parent is
            node.parent = self

        self._right = node

    @property
    def height(self):
        if self._height is None:
            self._height = self.calculate_height()
        return self._height

    @property
    def balance(self):
        left_height = self.left.height if self.left is not None else 0
        right_height = self.right.height if self.right is not None else 0
        return left_height - right_height

    def calculate_height(self):
        """
        Recursively calculate height of this node.
        Height calculated for each node will be stored, so calculations need to be done only once.
        :return: (int) Height of the current node
        """
        left_height = self.left.height if self.left is not None else 0
        right_height = self.right.height if self.right is not None else 0
        height = 1 + max(left_height, right_height)
        return height

    def update_height(self):
        """
        Recalculate the height of the node.
        """
        self._height = self.calculate_height()

    def update_heights(self):
        """
        Recalculate the heights of this node and all ancestor nodes.
        """

        # Calculate height
        self.update_height()

        # Update parent
        if self.parent is not None:
            self.parent.update_heights()

    def is_left_child(self):
        """
        Determines whether this node is a left child.
        :return: (bool) True if this node is a left child, False otherwise
        """
        if self.parent is None:
            return False
        return self.parent.left == self

    def is_right_child(self):
        """
        Determines whether this node is a right child.
        :return: (bool) True if this node is a right child, False otherwise
        """
        if self.parent is None:
            return False
        return self.parent.right == self

    def is_leaf(self):
        """
        Determines whether this node is a leaf.
        :return: (bool) True if this node is a leaf, False otherwise
        """
        return self.left is None and self.right is None

    def minimum(self):
        """
        Determines the node with the smallest key in the subtree rooted by this node.
        :return: (Node) Node with the smallest key
        """
        current = self
        while current.left is not None:
            current = current.left
        return current

    def maximum(self):
        """
        Determines the node with the largest key in the subtree rooted by this node.
        :return: (Node) Node with the largest key
        """
        current = self
        while current.right is not None:
            current = current.right
        return current

    @property
    def successor(self):
        """
        Returns the node with the smallest key larger than this node's key, or None
        if this node has the largest key in the tree.
        """

        # If the node has a right sub tree, take the minimum
        if self.right is not None:
            return self.right.minimum()

        # Walk up to the left until we are no longer a right child
        current = self
        while current.is_right_child():
            current = current.parent

        # Check there is a right branch
        if current.parent is None or current.parent.right is None:
            return None

        # Step over to the right branch, and take the minimum
        return current.parent.right.minimum()

    @property
    def predecessor(self):
        """
        Returns the node with the largest key smaller than this node's key, or None
        if this node has the smallest key in the tree.
        """

        # If the node has a left sub tree, take the maximum
        if self.left is not None:
            return self.left.maximum()

        # Walk up to the right until we are no longer a left child
        current = self
        while current.is_left_child():
            current = current.parent

        # Check there is a left branch
        if current.parent is None or current.parent.left is None:
            return None

        # Step over to the left branch, and take the maximum
        return current.parent.left.maximum()

    def replace_leaf(self, replacement, root):
        """
        Replace the node by a replacement tree.
        Requires the current node to be a leaf.

        :param replacement: (Node) The root node of the replacement sub tree
        :param root: (Node) The root of the tree
        :return: (Node) The root of the updated tree
        """

        # Give the parent of the node to the replacement
        if replacement is not None:
            replacement.parent = self.parent

        # If node is left child, replace it by giving the parent a new left node
        if self.is_left_child():
            self.parent.left = replacement

        # If node is right child, replace it by giving the parent a new right node
        elif self.is_right_child():
            self.parent.right = replacement

        # Otherwise, replace the root
        else:
            root = replacement

        # For non-empty replacement, start updating heights from replacement's root
        if replacement is not None:
            replacement.update_heights()

        # For empty replacement, start updating heights from the parent
        elif self.parent is not None:
            self.parent.update_heights()

        # Return the new tree. No need to return the replacement, because the
        # reference remains the same.
        return root

    def visualize(self):
        return self._visualize()

    def _visualize(self, depth=0):
        """
        Visualize the node and its descendants.

        :param depth: (int) Used by the recursive formula, should be left at the default value
        :return: (str) String representation of the visualization
        """
        ret = ""

        # Print right branch
        if self.right is not None:
            ret += self.right._visualize(depth + 1)

        # Print own value
        ret += "\n" + ("    " * depth) + str(self.get_label())

        # Print left branch
        if self.left is not None:
            ret += self.left._visualize(depth=depth + 1)

        return ret

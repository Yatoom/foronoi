# AVL Tree implementation
# - This AVL Tree is partially based on https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
#   but we have modified it and added more functionality.
# - We used some modified test cases to manually compare results from https://github.com/nlsdfnbch/Python-AVL-Tree/
from typing import Union

import pydot
from subprocess import Popen

from data_structures.types import Arc, Value, SimpleValue


class Node(object):
    def __init__(self, value):
        """
        A tree node that points to its left and right child and its parent.
        :param value: The content of the node
        """
        self.value: Value = value
        self._left = None
        self._right = None
        self.height = 1
        self.parent = None

    def __repr__(self):
        return f"Node({self.value}, left={self.left}, right={self.right})"

    def visualize(self, depth=0):
        ret = ""

        # Print right branch
        if self.right is not None:
            ret += self.right.visualize(depth + 1)

        # Print own value
        ret += "\n" + ("    "*depth) + str(self.value.get_name())

        # Print left branch
        if self.left is not None:
            ret += self.left.visualize(depth + 1)

        return ret

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, left):
        self._left = left
        if left is not None:
            self._left.parent = self

    @right.setter
    def right(self, right):
        self._right = right
        if right is not None:
            self._right.parent = self

    @property
    def children(self):
        return self.left, self.right

    @property
    def is_left_child(self):
        if self.parent is None:
            return False
        return self.parent.left == self

    @property
    def is_right_child(self):
        if self.parent is None:
            return False
        return self.parent.right == self

    def minimum(self):
        """
        Returns the node with the smallest key in the subtree rooted by this node.
        """
        current = self
        while current.left is not None:
            current = current.left
        return current

    def maximum(self):
        """
        Returns the node with the smallest key in the subtree rooted by this node.
        """
        current = self
        while current.right is not None:
            current = current.right
        return current

    def get_name(self):
        return self.value.name

    @property
    def successor(self):
        """
        Returns the node with the smallest key larger than this node's key, or None if this has the largest key in
        the tree.
        """
        if self.right is not None:
            return self.right.minimum()

        current = self
        while current.is_right_child:
            current = current.parent

        if current.parent is None or current.parent.right is None:
            return None

        return current.parent.right.minimum()

    @property
    def predecessor(self):
        """
        Returns the node with the largest key smaller than this node's key, or None if this has the largest key in
        the tree.
        """
        if self.left is not None:
            return self.left.maximum()

        current = self
        while current.is_left_child:
            current = current.parent

        if current.parent is None or current.parent.left is None:
            return None

        return current.parent.left.maximum()

    def replace(self, replacement, tree):
        replacement.parent = self.parent

        if self.is_left_child:
            self.parent.left = replacement
        elif self.is_right_child:
            self.parent.right = replacement
        else:
            tree.root = replacement

        tree.balance()
        return tree

    def disconnect(self, tree):
        if self.is_right_child:
            self.parent.right = None
        elif self.is_left_child:
            self.parent.left = None

        tree.balance()
        return tree


class AVLTree(object):
    def __init__(self):
        """
        Self-balancing Binary Search Tree.
        """
        self.root = None

    def find(self, key: int, state):
        """
        Find a node by binary search in the tree.

        :param key: (int) The key to search for
        :return: (Node or None) The found node, or None if there was no result
        """
        return AVLTree.find_in_subtree(root=self.root, key=key, state=state)

    def find_value(self, value: Value, state):
        node = self.root
        while node is not None:
            if value.get_key(state) == node.value.get_key(state):
                break
            elif value == node.value:
                break
            elif value.get_key(state) < node.value.get_key(state):
                node = node.left
            else:
                node = node.right

        # Return node, None if not found
        return node

    def visualize_tree(self):
        print(self.root.visualize())

    def find_arc_node(self, x, y):
        node = self.root
        key = x
        state = y

        while node is not None:
            if isinstance(node.value, Arc):
                return node
            if key == node.value.get_key(state):
                break
            elif key < node.value.get_key(state):
                node = node.left
            else:
                node = node.right

        # Return node, None if not found
        return node

    def visualize(self):
        """
        Simple visualization in text form.
        :return: (str) String of textual visualization.
        """
        graph = "digraph G {\n"
        result = ""
        nodes = [self.root]
        level_num = 0
        while len(nodes) > 0:
            level = []
            result += f"Level {level_num}\n"
            for position, node in enumerate(nodes):
                children = None
                if node is not None:
                    a, b = node.children
                    if a is not None:
                        graph += f"{node.value.get_name()}->{a.value.get_name()}\n"
                    if b is not None:
                        graph += f"{node.value.get_name()}->{b.value.get_name()}\n"
                    level.append(a)
                    level.append(b)
                    children = (len(level) - 2, len(level) - 1)
                result += f"{position} {node.value if node is not None else None} --> {children}\n"
            level_num += 1
            result += "\n"

            nodes = level
        graph += "}"
        f = open("graph.dot", 'w')
        f.write(graph)
        Popen(["dot", "-Tpng", "-o", "graph.png", "graph.dot"])
        return result

    @staticmethod
    def get_rightmost_leaf(root):

        node = root
        while node.right is not None:
            node = node.right

        return node

    @staticmethod
    def get_leftmost_leaf(root):

        node = root
        while node.left is not None:
            node = node.left

        return node

    def get_left_arc_node(self, arc_node):
        node = arc_node

        # Keep walking up until the node is a right child
        while node.is_right_child:
            node = node.parent

            # If there is no parent, we return None
            if node is None:
                return None

        # Once we are a right child, we check if we can switch to the left
        if node.parent is None or node.parent.left is None:
            return None

        # We are now on the left
        node = node.parent.left

        # Let's get the right most leaf from here
        node = self.get_rightmost_leaf(node)

        # Check if this is not the same node as we started with
        if node == arc_node:
            return None

        return self.get_rightmost_leaf(node)

    def get_right_arc_node(self, arc_node):
        node = arc_node

        # Keep walking up until the node is a left child
        while node.is_right_child:
            node = node.parent

            # If there is no parent, we return None
            if node is None:
                return None

        # Once we are a left child, we check if we can switch to the right
        if node.parent is None or node.parent.right is None:
            return None

        # We are now on the right
        node = node.parent.right

        # Let's get the right most leaf from here
        node = self.get_leftmost_leaf(node)

        # Check if this is not the same node as we started with
        if node == arc_node:
            return None

        return self.get_leftmost_leaf(node)

    def insert(self, value: Value, state):
        """
        Insert a node in the tree

        :param key: (int) The key to search for
        :param value: The content of the node
        :return: (Node or None) The found node, or None if there was no result
        """
        key = value.get_key(state)
        self.root = AVLTree.insert_in_subtree(root=self.root, key=key, value=value, state=state)

    def delete(self, key: int):
        """
        Recursive function to delete a node with given key from the tree.

        :param key: (int) The key of the node to search for and delete
        :return: (Node) the root of the modified subtree
        """
        self.root = AVLTree.delete_in_subtree(root=self.root, key=key)

    def __repr__(self):
        return self.root.__repr__()

    @staticmethod
    def find_in_subtree(root: Union[Node, None], key: int, state) -> Node:
        """
        Find a node using binary search on a given key, within a subtree.

        :param root: (Node) The root node of the subtree
        :param key: (int) The key to search for
        :return: (Node or None) The found node, or None if there was no result
        """

        node = root
        while node is not None:
            if key == node.value.get_key(state):
                break
            elif key < node.value.get_key(state):
                node = node.left
            else:
                node = node.right

        # Return node, None if not found
        return node

    @staticmethod
    def insert_in_subtree(root: Union[Node, None], key: int, value, state) -> Node:
        """
        Insert a node in a sub tree

        :param key: (int) The key to search for
        :param value: The content of the node
        :param root: (Node) The root node of the tree
        :return: (Node or None) The found node, or None if there was no result
        """

        # Normal Binary Search Tree insert
        if not root:
            return Node(value)
        elif key < root.value.get_key(state):
            root.left = AVLTree.insert_in_subtree(root.left, key, value, state)
        else:
            root.right = AVLTree.insert_in_subtree(root.right, key, value, state)

        # Update the height of the ancestor node
        AVLTree.update_height(root)

        # Get the balance factor
        balance = AVLTree.get_balance_factor(root)

        # If the node is unbalanced, then try out the 4 cases

        # Case 1 - Left Left
        if balance > 1 and key < root.left.value.get_key(state):
            return AVLTree.rotate_right(root)

        # Case 2 - Right Right
        if balance < -1 and key > root.right.value.get_key(state):
            return AVLTree.rotate_left(root)

        # Case 3 - Left Right
        if balance > 1 and key > root.left.value.get_key(state):
            root.left = AVLTree.rotate_left(root.left)
            return AVLTree.rotate_right(root)

        # Case 4 - Right Left
        if balance < -1 and key < root.right.value.get_key(state):
            root.right = AVLTree.rotate_right(root.right)
            return AVLTree.rotate_left(root)

        return root

    @staticmethod
    def delete_in_subtree(root: Union[Node, None], key: int) -> Node:
        """
        Recursive function to delete a node with given key from subtree with given root.
        :param root: (Node) The root of the (sub) tree
        :param key: (int) The key of the node to search for and delete
        :return: (Node) the root of the modified subtree
        """

        # Perform standard BST delete
        if not root:
            return root

        elif key < root.value.get_key():
            root.left = AVLTree.delete_in_subtree(root.left, key)

        elif key > root.value.get_key():
            root.right = AVLTree.delete_in_subtree(root.right, key)

        else:
            if root.left is None:
                return root.right

            elif root.right is None:
                return root.left

            temp = AVLTree.get_min_key_node(root.right)
            root.value = temp.value
            root.right = AVLTree.delete_in_subtree(root.right, temp.value.get_key())

        # If the tree has only one node, simply return it
        if root is None:
            return root

        # Update the height of the ancestor node
        AVLTree.update_height(root)

        # Balance the tree
        root = AVLTree._balance(root)

        return root

    def balance(self):
        # return self._balance(self.root)
        return self.root

    @staticmethod
    def _balance(root: Union[Node, None]) -> Node:
        """
        Make the three balanced if it is unbalanced.
        :param root: (Node) The root node of the tree to balance
        :return: (Node) The new root of the sub tree
        """
        balance = AVLTree.get_balance_factor(root)

        # If the node is unbalanced, then try out the 4 cases

        # Case 1 - Left Left
        if balance > 1 and AVLTree.get_balance_factor(root.left) >= 0:
            return AVLTree.rotate_right(root)

        # Case 2 - Right Right
        if balance < -1 and AVLTree.get_balance_factor(root.right) <= 0:
            return AVLTree.rotate_left(root)

        # Case 3 - Left Right
        if balance > 1 and AVLTree.get_balance_factor(root.left) < 0:
            root.left = AVLTree.rotate_left(root.left)
            return AVLTree.rotate_right(root)

        # Case 4 - Right Left
        if balance < -1 and AVLTree.get_balance_factor(root.right) > 0:
            root.right = AVLTree.rotate_right(root.right)
            return AVLTree.rotate_left(root)

        return root

    @staticmethod
    def rotate_left(z: Node) -> Node:
        """
        Rotate tree to the left.

        # T1, T2, T3 and T4 are subtrees.
        #     z                               y
        #    / \                            /  \
        #   T1   y     Left Rotate(z)      z     x
        #       / \   - - - - - - - ->   / \    / \
        #      T2  x                    T1  T2 T3  T4
        #         / \
        #       T3  T4

        :param z: (Node) The root of the sub tree
        :return: (Node) The new root of the sub tree
        """

        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        AVLTree.update_height(z)
        AVLTree.update_height(y)

        # Return the new root
        return y

    @staticmethod
    def rotate_right(z: Node) -> Node:
        """
        Rotate tree to the right.

        # T1, T2, T3 and T4 are subtrees.
        #          z                                      y
        #         / \                                   /   \
        #        y   T4      Right Rotate (z)          x      z
        #       / \          - - - - - - - - ->      /  \    /  \
        #      x   T3                               T1  T2  T3  T4
        #     / \
        #   T1   T2

        :param z: (Node) The root of the sub tree
        :return: (Node) The new root of the sub tree
        """

        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        AVLTree.update_height(z)
        AVLTree.update_height(y)

        # Return the new root
        return y

    @staticmethod
    def update_height(node: Node) -> Node:
        """
        Calculate the height of the node.
        :param node: The node for which to update the height
        :return: (Node) The given node with the updated height
        """
        node.height = 1 + max(AVLTree.get_height(node.left), AVLTree.get_height(node.right))
        return node

    @staticmethod
    def get_height(node: Node) -> int:
        """
        Get the height of the node, or 0 if the node is None.

        :param node: (Node) The node to determine the height for
        :return: (int) The height of the node
        """
        if not node:
            return 0

        return node.height

    @staticmethod
    def get_balance_factor(root):
        """
        The balance factor is defined to be the height difference of its two child subtrees.
        A binary tree is defined to be an AVL tree if the invariant BalanceFactor ∈ {–1,0,+1}
        holds for every node N in the tree.

        :param root: (Node) The root node to calculate balance for
        :return: (int) The calculated balance factor
        """
        if not root:
            return 0

        return AVLTree.get_height(root.left) - AVLTree.get_height(root.right)

    @staticmethod
    def get_min_key_node(root: Union[Node, None]) -> Node:
        """
        Get the node with the minimum key of the sub tree.

        :param root: (Node) The root node of the sub tree
        :return: (Node) The Node with the lowest key
        """

        if root is None or root.left is None:
            return root

        return AVLTree.get_min_key_node(root.left)

    @staticmethod
    def get_in_order_traversal(node: Node, node_list=None, keys_only=True) -> list:
        """
        Traverse the tree in order and return the result.

        :param node: (Node) The root node of the sub tree to traverse
        :param node_list: (list) List used for recursion that keeps track of the nodes
        :param keys_only: (bool) If True, return only the keys, rather than the Nodes
        :return: (list) THe list of nodes, in order of traversal
        """
        if node_list is None:
            node_list = []

        if node is not None:
            if keys_only:
                node_list.append(node.value.get_key())
            else:
                node_list.append(node)
            AVLTree.get_in_order_traversal(node.left, node_list)
            AVLTree.get_in_order_traversal(node.right, node_list)

        return node_list


# Manual testing. Can be converted to unit tests when needed.
if __name__ == '__main__':

    # Left-left case
    tree = AVLTree()

    values = [
        SimpleValue(5, (3, 5)),
        SimpleValue(3, (2, 3)),
        SimpleValue(2, (7, 2)),
    ]

    for value in values:
        tree.insert(value, state=None)

    # assert (tree.find(5, state=None).value == [3, 5])
    # assert (tree.find(7, state=None) is None)

    print(tree)
    print(tree.get_balance_factor(tree.root.right))

    # Right-right case
    tree = AVLTree()

    values = [
        SimpleValue(5, (3, 4)),
        SimpleValue(3, (2, 5)),
        SimpleValue(7, (7, 7)),
    ]

    for value in values:
        tree.insert(value, state=None)

    print(tree)
    print(tree.get_balance_factor(tree.root.right))

    # Left right case
    tree = AVLTree()

    values = [
        SimpleValue(5, (3, 5)),
        SimpleValue(3, (2, 3)),
        SimpleValue(4, (7, 4)),
    ]

    for value in values:
        tree.insert(value, state=None)

    print(tree)
    print(tree.get_balance_factor(tree.root.right))

    # Left right case
    tree = AVLTree()

    values = [
        SimpleValue(3, (3, 3)),
        SimpleValue(5, (2, 5)),
        SimpleValue(4, (7, 4)),
    ]

    for value in values:
        tree.insert(value, state=None)

    print(tree)
    print(tree.get_balance_factor(tree.root.right))

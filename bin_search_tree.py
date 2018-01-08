from typing import Union


class Node(object):
    def __init__(self, key, value):
        """
        A tree node that points to its left and right child and its parent.
        :param key: The value that the Binary Tree needs to sort on
        :param value: The content of the node
        """
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

    def __repr__(self):
        return f"Node({self.key}:{self.value}, left={self.left}, right={self.right})"


class AVLTree(object):

    @staticmethod
    def find(key: int, root: Union[Node, None]) -> Node:
        """
        Find a node using binary search on a given key.

        :param root: (Node) The root node of the tree
        :param key: (int) The key to search for
        :return: (Node or None) The found node, or None if there was no result
        """

        node = root
        while node is not None:
            if key == node.key:
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Return node, None if not found
        return node

    @staticmethod
    def insert(root: Union[Node, None], key: int, value) -> Node:
        """
        Find a node using binary search on a given key.

        :param key: (int) The key to search for
        :param value: The content of the node
        :param root: (Node) The root node of the tree
        :return: (Node or None) The found node, or None if there was no result
        """

        # Normal Binary Search Tree insert
        if not root:
            return Node(key, value)
        elif key < root.key:
            root.left = AVLTree.insert(root.left, key, value)
        else:
            root.right = AVLTree.insert(root.right, key, value)

        # Update the height of the ancestor node
        AVLTree.update_height(root)

        # Get the balance factor
        balance = AVLTree.get_balance(root)

        # If the node is unbalanced, then try out the 4 cases

        # Case 1 - Left Left
        if balance > 1 and key < root.left.key:
            return AVLTree.rotate_right(root)

        # Case 2 - Right Right
        if balance < -1 and key > root.right.key:
            return AVLTree.rotate_left(root)

        # Case 3 - Left Right
        if balance > 1 and key > root.left.key:
            root.left = AVLTree.rotate_left(root.left)
            return AVLTree.rotate_right(root)

        # Case 4 - Right Left
        if balance < -1 and key < root.right.key:
            root.right = AVLTree.rotate_right(root.right)
            return AVLTree.rotate_left(root)

        return root

    @staticmethod
    def delete(root: Union[Node, None], key: int) -> Node:
        """
        Recursive function to delete a node with given key from subtree with given root.
        :param root: (Node) The root of the (sub) tree
        :param key: (int) The key of the node to search for and delete
        :return: (Node) the root of the modified subtree
        """

        # Perform standard BST delete
        if not root:
            return root

        elif key < root.key:
            root.left = AVLTree.delete(root.left, key)

        elif key > root.key:
            root.right = AVLTree.delete(root.right, key)

        else:
            if root.left is None:
                return root.right

            elif root.right is None:
                return root.left

            temp = AVLTree.get_min_key_node(root.right)
            root.key = temp.key
            root.right = AVLTree.delete(root.right, temp.key)

        # If the tree has only one node, simply return it
        if root is None:
            return root

        # Update the height of the ancestor node
        AVLTree.update_height(root)

        # Balance the tree
        root = AVLTree.balance(root)

        return root

    @staticmethod
    def balance(root: Union[Node, None]) -> Node:
        """
        Make the three balanced if it is unbalanced.
        :param root: (Node) The root node of the tree to balance
        :return: (Node) The new root of the sub tree
        """
        balance = AVLTree.get_balance(root)

        # If the node is unbalanced, then try out the 4 cases

        # Case 1 - Left Left
        if balance > 1 and AVLTree.get_balance(root.left) >= 0:
            return AVLTree.rotate_right(root)

        # Case 2 - Right Right
        if balance < -1 and AVLTree.get_balance(root.right) <= 0:
            return AVLTree.rotate_left(root)

        # Case 3 - Left Right
        if balance > 1 and AVLTree.get_balance(root.left) < 0:
            root.left = AVLTree.rotate_left(root.left)
            return AVLTree.rotate_right(root)

        # Case 4 - Right Left
        if balance < -1 and AVLTree.get_balance(root.right) > 0:
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
    def get_balance(node):
        if not node:
            return 0

        return AVLTree.get_height(node.left) - AVLTree.get_height(node.right)

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
                node_list.append(node.key)
            else:
                node_list.append(node)
            AVLTree.get_in_order_traversal(node.left, node_list)
            AVLTree.get_in_order_traversal(node.right, node_list)

        return node_list


if __name__ == '__main__':
    tree = AVLTree()
    root_node = None

    values = {
        5: [3, 5],
        3: [2, 3],
        2: [7, 2]
    }

    for key, value in values.items():
        root_node = tree.insert(root_node, key=key, value=value)

    assert(AVLTree.find(5, root_node).value == [3, 5])
    assert(AVLTree.find(7, root_node) is None)
from voronoi.tree.smart_node import SmartNode


class SmartTree:
    """
    Self-balancing Binary Search Tree.
    """

    @staticmethod
    def find(root: SmartNode, key, **kwargs):

        node = root
        while node is not None:
            if key == node.get_key(**kwargs):
                break
            elif key < node.get_key(**kwargs):
                node = node.left
            else:
                node = node.right

        # Return node, None if not found
        return node

    @staticmethod
    def find_value(root: SmartNode, query: SmartNode, compare=lambda x, y: x == y, **kwargs):
        """
        Find an item using a query node and a comparison function.

        :param root: (SmartNode) The root to start searching from
        :param query: The query
        :param compare: (lambda) Lambda expression to compare the node against the query. Will be called as
        compare(node.data, query.data).
        :param kwargs: Optional arguments to be passed to the get_key() functions
        :return: (SmartNode or None) Returns the node that corresponds to the query or None
        """
        key = query.get_key(**kwargs)
        node = root
        while node is not None:
            if key == node.get_key(**kwargs):

                if compare(node.data, query.data):
                    return node

                left = SmartTree.find_value(node.left, query, compare, **kwargs)
                if left is None:
                    right = SmartTree.find_value(node.right, query, compare, **kwargs)
                    return right

                return left

            elif key < node.get_key(**kwargs):
                node = node.left
            else:
                node = node.right

        # Return node, None if not found
        return node

    @staticmethod
    def find_leaf_node(root: SmartNode, key, **kwargs):
        """
        Follows a path downward between the internal nodes using the key until it
        reaches a leaf node. If it is unclear which path to take, the left path is
        taken.

        :param root: (SmartNode) The root of the (sub)tree to travel down
        :param key: The key to use to determine the path
        :param kwargs: Optional arguments passed to the get_key() functions
        :return: (SmartNode) The node found at the end of the journey
        """

        node = root
        while node is not None:

            # If the node is a leaf, we have found a leaf
            if node.is_leaf():
                return node

            # If we found the key, we choose a direction
            elif key == node.get_key(**kwargs) and not node.is_leaf():

                # We take the left path if possible
                if node.left is not None:
                    return node.left.maximum()

                # Otherwise we take the right path
                return node.right.minimum()

            # Normal binary search
            elif key < node.get_key(**kwargs):
                node = node.left
            else:
                node = node.right

        # Return node, None if not found
        return node

    @staticmethod
    def insert(root: SmartNode, node: SmartNode, **kwargs):

        # Get keys once
        node_key = node.get_key(**kwargs) if node is not None else None
        root_key = root.get_key(**kwargs) if root is not None else None

        # Binary Search Tree insert
        if root is None:
            return node
        elif node_key < root_key:
            root.left = SmartTree.insert(root.left, node, **kwargs)
        else:
            root.right = SmartTree.insert(root.right, node, **kwargs)

        # Update the height of the ancestor node
        root.update_height()

        # If the node is unbalanced, then try out the 4 cases
        balance = root.balance
        # root = SmartTree.balance(root)

        # Case 1 - Left Left
        if balance > 1 and node_key < root.left.get_key(**kwargs):
            return SmartTree.rotate_right(root)

        # Case 2 - Right Right
        if balance < -1 and node_key > root.right.get_key(**kwargs):
            return SmartTree.rotate_left(root)

        # Case 3 - Left Right
        if balance > 1 and node_key > root.left.get_key(**kwargs):
            root.left = SmartTree.rotate_left(root.left)
            return SmartTree.rotate_right(root)

        # Case 4 - Right Left
        if balance < -1 and node_key < root.right.get_key(**kwargs):
            root.right = SmartTree.rotate_right(root.right)
            return SmartTree.rotate_left(root)

        return root

    @staticmethod
    def delete(root: SmartNode, key: int, **kwargs):

        if root is None:
            return root

        elif key < root.get_key():
            root.left = SmartTree.delete(root.left, key)

        elif key > root.get_key():
            root.right = SmartTree.delete(root.right, key)

        else:
            if root.left is None:
                return root.right

            elif root.right is None:
                return root.left

            temp = root.right.minimum()
            root.data = temp.data
            root.right = SmartTree.delete(root.right, temp.value.get_key(**kwargs))

        # If the tree has only one node, simply return it
        if root is None:
            return root

        # Update the height of the ancestor node
        root.update_height()

        # Balance the tree
        root = SmartTree.balance(root)

        return root

    @staticmethod
    def balance_and_propagate(node):
        """
        Walks up the tree recursively to rebalance all nodes, until it reaches the new root.

        :param node: The starting point, everything below this point is assumed to be balanced.
        :return: The root of the balanced tree
        """

        node = SmartTree.balance(node)

        if node.parent is None:
            return node

        return SmartTree.balance_and_propagate(node.parent)

    @staticmethod
    def balance(node):
        """
        Make the three balanced if it is unbalanced.
        :param node: (Node) The root node of the tree to balance
        :return: (Node) The new root of the sub tree
        """

        # If the node is unbalanced, then try out the 4 cases

        # Case 1 - Left Left
        if node.balance > 1 and node.left.balance >= 0:
            return SmartTree.rotate_right(node)

        # Case 2 - Right Right
        if node.balance < -1 and node.right.balance <= 0:
            return SmartTree.rotate_left(node)

        # Case 3 - Left Right
        if node.balance > 1 and node.left.balance < 0:
            node.left = SmartTree.rotate_left(node.left)
            return SmartTree.rotate_right(node)

        # Case 4 - Right Left
        if node.balance < -1 and node.right.balance > 0:
            node.right = SmartTree.rotate_right(node.right)
            return SmartTree.rotate_left(node)

        return node

    @staticmethod
    def rotate_left(z):
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
        grandparent = z.parent
        y = z.right
        T2 = y.left

        # Appoint new parent to root of sub tree
        y.parent = grandparent

        # And point the parent back
        if grandparent is not None:
            if z.is_left_child():
                grandparent.left = y
            else:
                grandparent.right = y

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights (z has to be updated first, because it is a child of y)
        z.update_height()
        y.update_height()

        # Return the new root
        return y

    @staticmethod
    def rotate_right(z):
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
        grandparent = z.parent
        y = z.left
        T3 = y.right

        # Appoint new parent to root of sub tree
        y.parent = grandparent

        # And point the parent back
        if grandparent is not None:
            if z.is_left_child():
                grandparent.left = y
            else:
                grandparent.right = y

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights (z has to be updated first, because it is a child of y)
        z.update_height()
        y.update_height()

        # Return the new root
        return y
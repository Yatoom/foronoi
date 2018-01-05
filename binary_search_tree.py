# AVL Tree implementation
# - This AVL Tree is partially based on https://github.com/nlsdfnbch/Python-AVL-Tree,
#   but we have modified it and added more functionality.
# - The ASCII illustrations come from http://blog.coder.si/2014/02/how-to-implement-avl-tree-in-python.html


class Node:
    """
    Self-balancing Binary Search Tree node.
    Attributes:
        value: value of the Node
        parent: Parent node of this Node
        is_root: Boolean, to determine if this Node is root
        left: Left child of this Node; Values smaller than price
        right: Right child of this Node; Values greater than price
    Properties:
        height: Height of this Node
        balance_factor: Balance factor of this Node
    """

    def __init__(self, key, value, is_root=False):
        """
        A tree node that points to its left and right child and its parent.
        :param key: The value that the Binary Tree needs to sort on
        :param value: The content of the node
        :param is_root: Flag for setting the root node
        """
        self.key = None if is_root else key
        self.value = None if is_root else value
        self.parent = None
        self.left = None
        self.right = None

        # Note that the root Node is not an actual node, but helps with rotating.
        # In Python it is impossible to do the following:
        #
        # def rotate_right():
        #   self.left.right = self
        #   self = self.left  <-- Not possible
        self.is_root = is_root

    @property
    def balance_factor(self):
        """
        The balance_factor factor is defined to be the height difference of its two child subtrees.
        A binary tree is defined to be an AVL tree if the invariant BalanceFactor ∈ {–1,0,+1}
        holds for every node N in the tree.

        :return: (int) balance_factor factor
        """
        right_height = 0 if self.right is None else self.right.height
        left_height = 0 if self.left is None else self.left.height
        return right_height - left_height

    @property
    def height(self):
        """
        Calculate the height of this node.
        :return: (int) height of the node
        """
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0

        return max(left_height, right_height) + 1

    def insert(self, key, value):
        """
        Insert a new value in the tree. The key determines the order in the tree.

        :param key: The value that the Binary Tree needs to sort on
        :param value: The content of the node
        :return: None
        """
        if self.key is None or key > self.key:
            if self.right is None:
                self.right = Node(key, value, is_root=False)
                self.right.parent = self
                self.right.balance_grandparent()
            else:
                self.right.insert(key, value)
        elif key < self.key:
            if self.left is None:
                self.left = Node(key, value, is_root=False)
                self.left.parent = self
                self.left.balance_grandparent()
            else:
                self.left.insert(key, value)

    def balance_grandparent(self):
        """
        Check if our grandparent needs rebalancing.
        :return: None
        """

        if self.parent is None or self.parent.parent is None:
            return
        elif not self.parent.parent.is_root:
            self.parent.parent.balance()
        return

    def balance(self):
        """
        Find out which rotation case we need, and balance_factor the tree.
        :return: (Node) self
        """
        if self.balance_factor > 1:

            # Right side is heavier
            if self.right.balance_factor < 0:
                self.rotate_rl()
            elif self.right.balance_factor > 0:
                self.rotate_rr()

        elif self.balance_factor < -1:

            # Left is heavier
            if self.left.balance_factor < 0:
                self.rotate_ll()
            elif self.left.balance_factor > 0:
                self.rotate_lr()

        return self

    def rotate_ll(self):
        """
        Rotate nodes for the lef-left case.

        # Left Left Case -> rotate z,x to the right
        #       x                 z
        #      / \              /   \
        #     z   D            y     x
        #    / \         ->   / \   / \
        #   y   C            A   B C   D
        #  / \
        # A   B

        :return: None
        """
        child = self.left

        if self.parent.is_root or self.value > self.parent.value:
            self.parent.right = child
        else:
            self.parent.left = child

        child.parent, self.parent = self.parent, child
        child.right, self.left = self, child.right

    def rotate_rr(self):
        """
        Rotate nodes for the right-right case.

        # Right Right Case -> rotate y,x to the left
        #       y                 z
        #      / \              /   \
        #     A   z            y     x
        #        / \     ->   / \   / \
        #       B   x        A   B C   D
        #          / \
        #         C   D

        :return: None
        """
        child = self.right

        if self.parent.is_root or self.value > self.parent.value:
            self.parent.right = child
        else:
            self.parent.left = child

        child.parent, self.parent = self.parent, child
        child.left, self.right = self, child.left

    def rotate_lr(self):
        """
        Rotate nodes for the lef-right case.

        # Left Right Case -> rotate y,z to the left
        #     x               x
        #    / \             / \
        #   y   D           z   D
        #  / \        ->   / \
        # A   z           y   C
        #    / \         / \
        #   B   C       A   B

        :return: None
        """
        child, grand_child = self.left, self.left.right
        child.parent, grand_child.parent = grand_child, self
        child.right = grand_child.left
        self.left, grand_child.left = grand_child, child
        self.rotate_ll()

    def rotate_rl(self):
        """
        Rotate nodes for the right-left case.

        # Right Left Case -> rotate x,z to the right
        #     y               y
        #    / \             / \
        #   A   x           A   z
        #      / \    ->       / \
        #     z   D           B   x
        #    / \                 / \
        #   B   C               C   D

        :return: None
        """
        child, grand_child = self.right, self.right.left
        child.parent, grand_child.parent = grand_child, self
        child.left = grand_child.right
        self.right, grand_child.right = grand_child, child
        self.rotate_rr()

    def __repr__(self):
        return f"Node({self.value}, left={self.left}, right={self.right})"


class AVLTree(Node):
    def __init__(self):
        super().__init__(None, None, is_root=True)

    def find(self, key):
        """
        Find a node using binary search on a given key.

        :param key: (int) The key to search for
        :return: (Node or None) The found node, or None if there was no result
        """
        node = self.right

        while node is not None:
            if key == node.key:
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Return node, None if not found
        return node


# Some testing... might want to use unit testing if used in a larger environment
if __name__ == '__main__':
    print("Testing Left Left Case")
    values = [5, 3, 2]
    print("Input", values)
    root = AVLTree()
    for v in values:
        root.insert(v, v)
        print(root)

    print("Found:", root.find(5))
    print("Not found:", root.find(7))

    print(root.right.balance_factor)
    print(root)
    print("----------")

    print("Testing Right Right Case")
    values = [3, 5, 7]
    print("Input", values)
    root = AVLTree()
    for v in values:
        root.insert(v, v)

    print(root.right.balance_factor)
    print(root)
    print("----------")

    print("Testing Left Right Case")
    values = [5, 3, 4]
    print("Input", values)
    root = AVLTree()
    for v in values:
        root.insert(v, v)

    print(root.right.balance_factor)
    print(root)
    print("----------")

    print("Testing Right Left Case")
    values = [3, 5, 4]
    print("Input", values)
    root = AVLTree()
    for v in values:
        root.insert(v, v)

    print(root.right.balance_factor)
    print(root)
    print("----------")

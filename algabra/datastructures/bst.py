from __future__ import annotations

import typing


class BinarySearchTree:
    __slots__ = ['_sentinel', '_length']

    def __init__(self) -> None:
        self._sentinel = SentinelNode()
        self._length = 0

    def search(self, key: int) -> typing.Optional[Node]:
        result = self._get_root()
        while result is not self._sentinel and result.key != key:
            result = result.left if key < result.key else result.right

        return None if result is self._sentinel else result

    def minimum(self, node: Node = None) -> typing.Optional[Node]:
        result = self._get_root() if node is None else node
        while result.left != self._sentinel:
            result = result.left

        return None if result is self._sentinel else result

    def maximum(self, node: Node = None) -> typing.Optional[Node]:
        result = self._get_root() if node is None else node
        while result.right != self._sentinel:
            result = result.right

        return None if result is self._sentinel else result

    def predecessor(self, node: Node) -> typing.Optional[Node]:
        if node.left is not self._sentinel:
            return self.maximum(node.left)

        result = node.parent
        child = node
        while result is not self._sentinel and child == result.left:
            child = result
            result = result.parent

        return None if result is self._sentinel else result

    def successor(self, node: Node) -> typing.Optional[Node]:
        if node.right is not self._sentinel:
            return self.minimum(node.right)

        result = node.parent
        child = node
        while result is not self._sentinel and child == result.right:
            child = result
            result = result.parent

        return None if result is self._sentinel else result

    def insert(self, node: Node) -> None:
        child = self._get_root()
        parent = self._sentinel

        while child != self._sentinel:
            parent = child
            child = parent.left if node.key < parent.key else parent.right

        node.left = node.right = self._sentinel
        node.parent = parent
        if parent is self._sentinel or parent.key < node.key:
            parent.right = node
        else:
            parent.left = node

        self._length += 1

    def delete(self, node: Node) -> None:
        if node.left is self._sentinel:
            self._replace(node, node.right)
        elif node.right is self._sentinel:
            self._replace(node, node.left)
        else:
            successor = self.minimum(node.right)
            if successor.parent is not node:
                self._replace(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
            self._replace(node, successor)
            successor.left = node.left
            successor.left.parent = successor

        self._length -= 1

    def __len__(self) -> int:
        return self._length

    def __iter__(self):
        next_node = self.minimum()
        while next_node is not None:
            yield next_node
            next_node = self.successor(next_node)

    def _get_root(self) -> Node:
        return self._sentinel.right

    def _replace(self, node: Node, replacement: Node) -> None:
        if node is node.parent.left:
            node.parent.left = replacement
        else:
            node.parent.right = replacement

        if replacement is not self._sentinel:
            replacement.parent = node.parent


class RightRotation(object):

    @staticmethod
    def rotate(root: Node) -> Node:
        if root.parent.left == root:
            root.parent.left = root.left
        else:
            root.parent.right = root.left

        root.parent, root.left.parent = root.left, root.parent
        root.left.right, root.left = root, root.left.right

        if not isinstance(root.left, SentinelNode):
            root.left.parent = root

        return root.parent


class LeftRotation(object):

    @staticmethod
    def rotate(root: Node) -> Node:
        if root.parent.left == root:
            root.parent.left = root.right
        else:
            root.parent.right = root.right

        root.right.parent, root.parent = root.parent, root.right
        root.right.left, root.right = root, root.right.left

        if not isinstance(root.right, SentinelNode):
            root.right.parent = root

        return root.parent


class AVLTree(BinarySearchTree):
    MAX_HEIGHT_DELTA = 1
    _ZERO_HEIGHT = 0

    def insert(self, node: AVLNode) -> None:
        super().insert(node)
        self._balance(node.parent)

    def delete(self, node: Node) -> None:
        super().delete(node)
        self._balance(node.parent)

    def _balance(self, root: AVLNode) -> None:
        while isinstance(root, AVLNode):
            root.height = self._calculate_height(root)
            balance = self._get_balance(root)
            if balance > self.MAX_HEIGHT_DELTA:
                if self._get_balance(root.left) < 0:
                    self._rotate_left(root.left)
                root = self._rotate_right(root)
            if balance < -self.MAX_HEIGHT_DELTA:
                if self._get_balance(root.right) > 0:
                    self._rotate_right(root.right)
                root = self._rotate_left(root)

            root = root.parent

    def _rotate_right(self, root: AVLNode) -> AVLNode:
        new_root = RightRotation.rotate(root)
        root.height = self._calculate_height(root)
        new_root.height = self._calculate_height(new_root)

        return new_root

    def _rotate_left(self, root: AVLNode) -> AVLNode:
        new_root = LeftRotation.rotate(root)
        root.height = self._calculate_height(root)
        new_root.height = self._calculate_height(new_root)

        return new_root

    def _calculate_height(self, root: AVLNode) -> int:
        return AVLNode.INITIAL_HEIGHT + max(
            self._get_height(root.right), self._get_height(root.left))

    def _get_height(self, node: Node) -> int:
        return node.height if isinstance(node, AVLNode) else self._ZERO_HEIGHT

    def _get_balance(self, node: AVLNode) -> int:
        return self._get_height(node.left) - self._get_height(node.right)


T = typing.TypeVar('T')


class Node():
    __slots__ = ['left', 'right', 'parent', 'key']

    def __init__(self, key: int = None) -> None:
        self.key = key


class AVLNode(Node):
    INITIAL_HEIGHT = 1

    __slots__ = 'height'

    def __init__(self, key: int = None) -> None:
        super().__init__(key)
        self.height = self.INITIAL_HEIGHT


class SentinelNode(Node):

    def __init__(self) -> None:
        super().__init__()
        self.left = self
        self.right = self
        self.parent = self

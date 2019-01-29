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
        parent = child.parent

        while child != self._sentinel:
            parent = child
            child = child.left if node.key < child.key else child.right

        node.parent = parent
        node.left = child
        node.right = child
        if parent is self._sentinel or parent.key < node.key:
            parent.right = node
        else:
            parent.left = node

        self._length += 1

    def delete(self, node: Node) -> None:
        if node.left is self._sentinel:
            self._transplant(node, node.right)
        elif node.right is self._sentinel:
            self._transplant(node, node.left)
        else:
            successor = self.minimum(node.right)
            if successor.parent is not node:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
            self._transplant(node, successor)
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

    def _transplant(self, node: Node, transplant: Node) -> None:
        if node is node.parent.left:
            node.parent.left = transplant
        else:
            node.parent.right = transplant

        if transplant is not self._sentinel:
            transplant.parent = node.parent


class Node:
    __slots__ = ['left', 'right', 'parent', 'key']

    def __init__(self, key: int = None) -> None:
        self.key = key


class SentinelNode(Node):

    def __init__(self) -> None:
        super().__init__()
        self.left = self
        self.right = self
        self.parent = self

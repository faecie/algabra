from __future__ import annotations

import typing


class LinkedList:
    __slots__ = ['_sentinel']

    def __init__(self) -> None:
        self._sentinel = SentinelNode()
        self._sentinel.key = None

    def search(self, key) -> typing.Optional[Node]:
        result = self._sentinel.next
        while result != self._sentinel and result.key != key:
            result = result.next

        return None if result is self._sentinel else result

    def insert(self, node: Node) -> None:
        node.next = self._sentinel.next
        self._sentinel.next.prev = node
        self._sentinel.next = node
        node.prev = self._sentinel

    def delete(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def minimum(self) -> Node:
        return None if self._sentinel.prev is self._sentinel else self._sentinel.prev

    def maximum(self) -> Node:
        return None if self._sentinel.next is self._sentinel else self._sentinel.next

    def successor(self, node: Node) -> typing.Optional[Node]:
        return node.prev if node.prev is not self._sentinel else None

    def predecessor(self, node: Node) -> Node:
        return node.next if node.next is not self._sentinel else None


class Node:
    __slots__ = ['key', 'prev', 'next']

    def __init__(self, key: int = None) -> None:
        self.key = key


class SentinelNode(Node):

    def __init__(self) -> None:
        super().__init__()
        self.next = self
        self.prev = self

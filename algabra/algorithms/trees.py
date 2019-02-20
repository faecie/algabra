import collections


class Tree:
    ROOT_KEY = 1

    __slots__ = 'sentinel', 'root'

    def __init__(self) -> None:
        self.sentinel = SentinelNode()
        self.root = Node(self.ROOT_KEY)
        self.root.parent = self.sentinel

    @staticmethod
    def build_tree(nodes) -> 'Tree':
        tree = Tree()
        nodes_queue = collections.deque()
        nodes_queue.appendleft(tree.root)
        for children in nodes:
            node = nodes_queue.popleft()
            left = tree.add_left_child(node, children[0])
            right = tree.add_right_child(node, children[1])
            if not isinstance(left, SentinelNode):
                nodes_queue.append(left)
            if not isinstance(right, SentinelNode):
                nodes_queue.append(right)

        return tree

    def swap(self, coefficient):
        height = 1
        nodes = collections.deque()
        nodes.append(self.root)
        children = collections.deque()
        while len(nodes) > 0:
            node = nodes.popleft()
            if height % coefficient == 0:
                node.left, node.right = node.right, node.left
            if not isinstance(node.left, SentinelNode):
                children.append(node.left)
            if not isinstance(node.right, SentinelNode):
                children.append(node.right)

            if len(nodes) == 0:
                nodes, children = children, nodes
                height += 1

    def traverse_inorder(self):
        first = self.root
        while not isinstance(first.left, SentinelNode):
            first = first.left

        while not isinstance(first, SentinelNode):
            yield first.key

            if not isinstance(first.right, SentinelNode):
                first = first.right
                while not isinstance(first.left, SentinelNode):
                    first = first.left
            else:
                child = first
                first = first.parent
                while not isinstance(first,
                                     SentinelNode) and child == first.right:
                    child = first
                    first = first.parent

    def add_left_child(self, parent: 'Node', key: int) -> 'Node':
        parent.left = self.require_node(key)
        parent.left.parent = parent

        return parent.left

    def add_right_child(self, parent: 'Node', key: int) -> 'Node':
        parent.right = self.require_node(key)
        parent.right.parent = parent

        return parent.right

    def require_node(self, key) -> 'Node':
        if key == SentinelNode.SENTINEL_KEY:
            return self.sentinel
        else:
            node = Node(key)

            return node


class Node:
    __slots__ = 'parent', 'left', 'right', 'key'

    def __init__(self, key):
        self.key = key


class SentinelNode(Node):
    SENTINEL_KEY = -1

    def __init__(self):
        super().__init__(self.SENTINEL_KEY)

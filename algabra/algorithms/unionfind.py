class Component:
    __slots__ = 'parent', 'size', 'key'

    def __init__(self) -> None:
        self.size = 1
        self.parent = self

    def connect(self, other: 'Component'):
        selfroot = self.get_root()
        othersroot = other.get_root()

        if selfroot == othersroot:
            return

        if selfroot.size < othersroot.size:
            selfroot.parent = othersroot
            othersroot.size += selfroot.size
        else:
            othersroot.parent = selfroot
            selfroot.size += othersroot.size

    def get_root(self) -> 'Component':
        root = self
        while root != root.parent:
            root.parent = root.parent.parent
            root = root.parent
        return root


class ComponentMatrix:
    __slots__ = '_open_components', '_rows', '_cols', '_matrix'

    def __init__(self, matrix: list) -> None:
        self._open_components = dict()
        self._rows = len(matrix)
        self._cols = len(matrix[0])
        self._matrix = matrix

    def require(self, i: int, j: int):
        if not self.is_open(i, j):
            raise IndexError('Component %d:%d is closed or not in the matrix' % (i, j))
        key = '%d%d' % (i, j)
        if key not in self._open_components:
            self._open_components[key] = Component()
        return self._open_components[key]

    def is_open(self, i, j) -> bool:
        if self.in_matrix(i, j) and self._matrix[i][j] == 1:
            return True
        return False

    def in_matrix(self, i, j) -> bool:
        if 0 <= i < self._rows and 0 <= j < self._cols:
            return True
        return False


def connected_cell(matrix):
    components = ComponentMatrix(matrix)
    max_size = 0
    for i in range(0, len(matrix)):
        for j in range(len(matrix[i])):
            if not components.is_open(i, j):
                continue
            component = components.require(i, j)
            adjacent_components = [
                (i, j - 1), (i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
                (i, j + 1), (i + 1, j + 1), (i + 1, j), (i + 1, j - 1)
            ]
            for adjacent in adjacent_components:
                if components.is_open(*adjacent):
                    component.connect(components.require(*adjacent))
            size = component.get_root().size
            max_size = size if size > max_size else max_size

    return max_size

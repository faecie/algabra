import typing


class MyArray(typing.MutableSequence):
    __slots__ = ['_length', '_values', '_elements_count']

    @typing.overload
    def __init__(self, values: typing.Iterator) -> None:
        pass

    @typing.overload
    def __init__(self, size: int = 0) -> None:
        pass

    def __init__(self, init=0) -> None:
        iterable = init if isinstance(init, typing.Iterable) else [None] * init
        self._length = 0
        self._elements_count = 0
        self._values = []
        for value in iterable:
            self._values.append(value)
            self._length += 1 if value is not None else 0
            self._elements_count += 1

    def __getitem__(self, i: int) -> typing.Any:
        self._validate_index(i)
        return self._values[i]

    def __setitem__(self, index: int, value) -> None:
        self._validate_index(index)
        original_value = self._values[index]
        self._values[index] = value
        self._length += 1 if value != original_value is None else 0

    def __delitem__(self, i: int) -> None:
        self._validate_index(i)
        original_value = self._values[i]
        self._values[i] = None
        self._length -= 1 if original_value is not None else 0

    def __len__(self) -> int:
        return self._length

    def _validate_index(self, index) -> None:
        if index > self._elements_count - 1:
            raise IndexError

    def insert(self, index: int, value) -> None:
        self.__setitem__(index, value)


class FixedArray(MyArray):
    pass


class RubberArray(MyArray):

    def __setitem__(self, index: int, value) -> None:
        if self._elements_count < index:
            self._extend(index)
        super().__setitem__(index, value)

    def __delitem__(self, i: int) -> None:
        super().__delitem__(i)
        if self._length < self._elements_count / 4:
            self._reduce()

    def _reduce(self) -> None:
        self._values = list(filter(lambda x: x is not None, self._values))
        self._values += [None] * self._length
        self._elements_count = len(self._values)

    def _extend(self, index) -> None:
        self._values += [None] * (self._length + index * 2)
        self._elements_count = len(self._values)

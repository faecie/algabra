import typing


class FixedArray:
    __slots__ = ['_length', '_values']

    @typing.overload
    def __init__(self, values: typing.Iterator) -> None:
        pass

    @typing.overload
    def __init__(self, length: int = 0) -> None:
        pass

    def __init__(self, value=0) -> None:
        is_iterable = isinstance(value, typing.Iterable)
        self._values = list(value) if is_iterable else [None] * value
        self._length = len(self._values)

    def __getitem__(self, i: int) -> typing.Any:
        self._validate_index(i)

        return self._values[i]

    def __setitem__(self, index: int, value) -> None:
        self._validate_index(index)
        self._values[index] = value

    def __delitem__(self, i: int) -> None:
        self._validate_index(i)
        self._values[i] = None

    def _validate_index(self, index) -> None:
        if index > self._length:
            raise IndexError

    def __len__(self) -> int:
        return self._length

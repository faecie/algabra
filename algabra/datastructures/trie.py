import typing


class Trie(object):
    __slots__ = '_root'

    def __init__(self, words: typing.List[str]) -> None:
        self._root = RootNode()
        for word in words:
            self._root.put_prefix(word).set_terminal()

    def has_word(self, word: str) -> bool:
        node = self._root.get_prefix(word)

        return bool(node and node.is_terminal())

    def has_prefix(self, prefix: str) -> bool:
        return isinstance(self._root.get_prefix(prefix), TrieNode)


class TrieNode(object):
    __slots__ = '_letters', '_value', '_is_terminal'

    def __init__(self, value: str) -> None:
        self._letters: typing.Dict[str, 'TrieNode'] = dict()
        self._value = value
        self._is_terminal = False

    def get_prefix(self, prefix: str) -> typing.Optional['TrieNode']:
        first_letter = prefix[:1]
        if first_letter in self._letters:
            node = self._letters[first_letter]
            pfx_len = len(prefix)
            return node.get_prefix(prefix[1:]) if pfx_len > 1 else node

        return None

    def put_prefix(self, prefix: str) -> 'TrieNode':
        first_letter = prefix[:1]
        pfx_len = len(prefix)
        if first_letter not in self._letters:
            self._letters[first_letter] = TrieNode(first_letter)
        if pfx_len > 1:
            return self._letters[first_letter].put_prefix(prefix[1:])

        return self._letters[first_letter]

    def is_terminal(self) -> bool:
        return self._is_terminal

    def set_terminal(self, is_terminal: bool = True) -> None:
        self._is_terminal = is_terminal


class RootNode(TrieNode):

    def __init__(self) -> None:
        super().__init__('')

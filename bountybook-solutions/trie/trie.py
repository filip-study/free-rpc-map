"""Prefix tree for case-sensitive word lookup."""


class _Node:
    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    """Store words and answer exact-match and prefix queries."""

    def __init__(self):
        self._root = _Node()
        self._count = 0

    def insert(self, word):
        """Add `word` to the trie. Inserting it again is a no-op."""
        if not isinstance(word, str) or word == "":
            raise ValueError("word must be a non-empty string")
        node = self._root
        for character in word:
            child = node.children.get(character)
            if child is None:
                child = _Node()
                node.children[character] = child
            node = child
        if not node.is_word:
            node.is_word = True
            self._count += 1

    def search(self, word):
        """Return True only when `word` was inserted exactly."""
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix):
        """Return True when some inserted word begins with `prefix`.

        An empty prefix is True once the trie holds at least one word.
        """
        if prefix == "":
            return self._count > 0
        return self._walk(prefix) is not None

    def _walk(self, text):
        node = self._root
        for character in text:
            node = node.children.get(character)
            if node is None:
                return None
        return node

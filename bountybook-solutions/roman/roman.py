"""Convert integers in 1..3999 to and from Roman numerals."""

_VALUES = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

_SYMBOLS = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def to_roman(n):
    """Convert an integer from 1 through 3999 into a Roman numeral."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer in 1..3999")
    if n < 1 or n > 3999:
        raise ValueError("n must be an integer in 1..3999")

    remaining = n
    parts = []
    for value, glyph in _VALUES:
        count, remaining = divmod(remaining, value)
        if count:
            parts.append(glyph * count)
    return "".join(parts)


def from_roman(s):
    """Convert a Roman numeral string into an integer.

    Invalid characters, empty strings, and numerals that do not follow the
    standard subtractive form raise ValueError.
    """
    if not isinstance(s, str) or not s:
        raise ValueError("invalid roman numeral")

    total = 0
    index = 0
    length = len(s)
    while index < length:
        current = _SYMBOLS.get(s[index])
        if current is None:
            raise ValueError("invalid roman numeral")
        if index + 1 < length:
            nxt = _SYMBOLS.get(s[index + 1])
            if nxt is None:
                raise ValueError("invalid roman numeral")
            if nxt > current:
                total += nxt - current
                index += 2
                continue
        total += current
        index += 1

    if total < 1 or total > 3999 or to_roman(total) != s:
        raise ValueError("invalid roman numeral")
    return total

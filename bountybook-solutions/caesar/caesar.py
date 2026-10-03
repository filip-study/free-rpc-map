"""Caesar cipher encode and decode.

Only alphabetic characters move. Case is preserved, and everything else
(spaces, digits, punctuation) is copied through unchanged. The shift wraps
inside each alphabet, so 'z' shifted by 3 is 'c'.
"""


def _shift_char(character, shift):
    """Shift one character by `shift` positions, or return it unchanged."""
    if "a" <= character <= "z":
        base = ord("a")
    elif "A" <= character <= "Z":
        base = ord("A")
    else:
        return character
    offset = (ord(character) - base + shift) % 26
    return chr(base + offset)


def encode(text, shift):
    """Encode `text` by rotating letters `shift` places."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    amount = int(shift)
    return "".join(_shift_char(character, amount) for character in text)


def decode(text, shift):
    """Reverse `encode` by rotating letters the other way."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    amount = int(shift)
    return encode(text, -amount)

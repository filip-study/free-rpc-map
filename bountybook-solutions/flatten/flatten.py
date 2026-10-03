"""Flatten nested dictionaries into a single mapping."""


def flatten_dict(d, sep="."):
    """Return a one-level dict whose keys join nested keys with `sep`.

    Nested dicts are walked recursively. An empty nested dict contributes
    no keys. Lists, numbers, strings, None, and any other non-dict value
    are stored as-is and are not expanded.
    """
    if not isinstance(d, dict):
        raise TypeError("expected a dict")
    if not isinstance(sep, str):
        raise TypeError("sep must be a string")

    flat = {}

    def walk(prefix, obj):
        for key, value in obj.items():
            path = f"{prefix}{sep}{key}" if prefix else str(key)
            if isinstance(value, dict):
                if value:
                    walk(path, value)
                continue
            flat[path] = value

    walk("", d)
    return flat

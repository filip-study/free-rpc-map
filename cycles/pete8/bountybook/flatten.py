def flatten_dict(d: dict, sep: str = ".") -> dict:
    """Flatten nested dicts. Empty nested dicts contribute no keys."""
    if not isinstance(d, dict):
        raise TypeError("expected a dict")

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

"""Render a list of uniform dictionaries as a GitHub-flavored Markdown table."""


def json_to_markdown_table(data):
    """Build a Markdown table from a non-empty list of dicts.

    Column order follows the first dict. Cells are `str()` of the value.
    The separator row is dashes only. Each row ends with a newline, and
    cells use a single space of padding inside the pipes.
    """
    if not isinstance(data, list) or not data:
        raise ValueError("data must be a non-empty list of dicts")
    first = data[0]
    if not isinstance(first, dict) or not first:
        raise ValueError("rows must be non-empty dicts")

    columns = list(first.keys())

    def format_row(cells):
        body = " | ".join(str(cell) for cell in cells)
        return f"| {body} |\n"

    lines = [
        format_row(columns),
        format_row(["---"] * len(columns)),
    ]
    for row in data:
        if not isinstance(row, dict):
            raise ValueError("rows must be dicts")
        lines.append(format_row(row.get(column) for column in columns))
    return "".join(lines)

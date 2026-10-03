"""Parse Apache common/combined log lines into structured records."""

import re

_LINE = re.compile(
    r"^(?P<ip>\S+)\s+\S+\s+(?P<user>\S+)\s+\[(?P<timestamp>[^\]]+)\]\s+"
    r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<protocol>[^"]+)"\s+'
    r"(?P<status>\d+)\s+(?P<bytes>\S+)"
)


def parse_log(log_text):
    """Return one dict per well-formed log line.

    Lines that do not match are skipped. A user of '-' becomes None.
    A byte count of '-' becomes 0. The timestamp is kept as written.
    """
    if log_text is None:
        raise TypeError("log_text must be a string")

    rows = []
    for raw_line in str(log_text).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = _LINE.match(line)
        if match is None:
            continue
        user = match.group("user")
        size = match.group("bytes")
        rows.append(
            {
                "ip": match.group("ip"),
                "user": None if user == "-" else user,
                "timestamp": match.group("timestamp"),
                "method": match.group("method"),
                "path": match.group("path"),
                "protocol": match.group("protocol"),
                "status": int(match.group("status")),
                "bytes": 0 if size == "-" else int(size),
            }
        )
    return rows

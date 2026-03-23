import re

_HTML_TAG_RE = re.compile(r"<[^>]+>")


def clean(lines: list[str]) -> list[str]:
    result = []
    prev = None

    for line in lines:
        line = _HTML_TAG_RE.sub("", line).strip()

        if not line:
            continue

        if line == prev:
            continue

        result.append(line)
        prev = line

    return result

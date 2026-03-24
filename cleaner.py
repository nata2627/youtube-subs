import re

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_MULTI_SPACE_RE = re.compile(r" {2,}")
_SPACE_BEFORE_PUNCT_RE = re.compile(r" +([,\.!?;:])")
_MUSIC_RE = re.compile(r"[♪♫]")


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            curr.append(min(
                prev[j] + 1,
                curr[j - 1] + 1,
                prev[j - 1] + (0 if ca == cb else 1),
            ))
        prev = curr
    return prev[-1]


def _is_duplicate(line: str, recent: list[str], threshold: float = 0.2) -> bool:
    for prev in recent:
        max_len = max(len(line), len(prev))
        if max_len == 0:
            continue
        dist = _levenshtein(line, prev)
        if dist / max_len <= threshold:
            return True
    return False


def clean(lines: list[str]) -> list[str]:
    result = []
    recent: list[str] = []

    for line in lines:
        line = _HTML_TAG_RE.sub("", line)
        line = _MUSIC_RE.sub("", line)
        line = _MULTI_SPACE_RE.sub(" ", line)
        line = _SPACE_BEFORE_PUNCT_RE.sub(r"\1", line)
        line = line.strip()

        if not line:
            continue

        if _is_duplicate(line, recent[-5:]):
            continue

        result.append(line)
        recent.append(line)

    return result

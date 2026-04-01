import re


_TIMING_RE = re.compile(r"^[\d:.]+\s*-->")


def parse_vtt(text: str) -> list[str]:
    """
    Parse a WebVTT subtitle file and return a list of text lines.

    Splits the file into blocks separated by blank lines and processes each
    block individually. Skips the WEBVTT header, NOTE/REGION/STYLE blocks,
    cue identifiers (numeric or text), and timing lines. Strips all inline
    tags (e.g. <b>, <c>, <00:00:01.000>) from cue text lines.
    """
    raw_blocks = re.split(r"\n[ \t]*\n", text.strip())
    result = []

    for idx, block in enumerate(raw_blocks):
        lines = [ln.rstrip() for ln in block.strip().splitlines()]
        if not lines:
            continue

        first = lines[0]

        if idx == 0 and first.startswith("WEBVTT"):
            continue

        if first.startswith(("NOTE", "REGION", "STYLE")):
            continue

        timing_idx = None
        for j, ln in enumerate(lines):
            if _TIMING_RE.match(ln.strip()):
                timing_idx = j
                break

        if timing_idx is None:
            continue

        for ln in lines[timing_idx + 1:]:
            clean = re.sub(r"<[^>]*>", "", ln).strip()
            if clean:
                result.append(clean)

    return result


def parse_srt(text: str) -> list[str]:
    """
    Parse an SRT subtitle file and return a list of text lines.

    Strips numeric cue indices, timing lines (HH:MM:SS,mmm --> HH:MM:SS,mmm),
    and blank separators. Returns only the actual subtitle text lines.
    """
    lines = text.splitlines()
    result = []

    timing_re = re.compile(
        r"^\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}"
    )
    index_re = re.compile(r"^\d+$")

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if index_re.match(stripped):
            continue

        if timing_re.match(stripped):
            continue

        clean = re.sub(r"<[^>]+>", "", stripped)
        clean = clean.strip()
        if clean:
            result.append(clean)

    return result


def detect_format(text: str) -> str:
    first_line = text.lstrip().split("\n")[0].strip()
    if first_line.startswith("WEBVTT"):
        return "vtt"

    srt_timing_re = re.compile(
        r"^\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}"
    )
    index_re = re.compile(r"^\d+$")
    lines = text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if index_re.match(stripped) and i + 1 < len(lines):
            if srt_timing_re.match(lines[i + 1].strip()):
                return "srt"

    return "unknown"


def parse(text: str, fmt: str) -> list[str]:
    """
    Dispatch to the appropriate parser based on subtitle format.

    Supported formats: 'vtt', 'srt'. Unknown formats are passed through
    as a single-element list containing the raw text.
    """
    if fmt == "vtt":
        return parse_vtt(text)
    if fmt == "srt":
        return parse_srt(text)
    return [line.strip() for line in text.splitlines() if line.strip()]

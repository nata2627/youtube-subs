import re


def parse_vtt(text: str) -> list[str]:
    """
    Parse a WebVTT subtitle file and return a list of text lines.

    Strips the WEBVTT header, NOTE/REGION blocks, cue timings, and cue
    identifiers. Returns only the actual subtitle text lines.
    """
    lines = text.splitlines()
    result = []

    # Skip the mandatory WEBVTT header line (and optional header metadata
    # that may follow before the first blank line).
    i = 0
    if lines and lines[0].startswith("WEBVTT"):
        i += 1
        # Consume any continuation lines of the header block.
        while i < len(lines) and lines[i].strip():
            i += 1

    timing_re = re.compile(
        r"^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}"
    )
    # Also accept timestamps without hours: MM:SS.mmm --> MM:SS.mmm
    timing_re_short = re.compile(
        r"^\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}\.\d{3}"
    )
    cue_id_re = re.compile(r"^\d+$")

    in_note_region = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Track NOTE / REGION block boundaries.
        if stripped.startswith("NOTE") or stripped.startswith("REGION"):
            in_note_region = True
            i += 1
            continue

        # A blank line ends any active NOTE/REGION block.
        if not stripped:
            in_note_region = False
            i += 1
            continue

        # Skip lines that are inside a NOTE or REGION block.
        if in_note_region:
            i += 1
            continue

        # Skip cue timing lines (with optional trailing positioning tags).
        if timing_re.match(stripped) or timing_re_short.match(stripped):
            i += 1
            continue

        # Skip numeric-only cue identifiers.
        if cue_id_re.match(stripped):
            i += 1
            continue

        # What remains is subtitle text. Strip inline tags like <c>, <b>, etc.
        clean = re.sub(r"<[^>]+>", "", stripped)
        clean = clean.strip()
        if clean:
            result.append(clean)

        i += 1

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

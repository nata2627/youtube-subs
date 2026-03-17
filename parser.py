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

import urllib.request

import yt_dlp


def fetch_subtitles(url: str, lang: str) -> tuple[str, str]:
    """
    Download subtitles for a YouTube video into memory without writing to disk.

    Returns a (raw_text, fmt) tuple where fmt is the subtitle format string
    (e.g. 'vtt' or 'srt').  Raises ValueError when no subtitles are available
    for the requested language.
    """
    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Manual subtitles take priority over auto-generated captions.
    subtitles = info.get("subtitles", {})
    auto_captions = info.get("automatic_captions", {})

    sub_formats = subtitles.get(lang) or auto_captions.get(lang)

    if not sub_formats:
        raise ValueError(f"No subtitles found for language '{lang}'")

    # Pick the best available format — vtt preferred, then srt, then first in list.
    preferred = ["vtt", "srt"]
    chosen = None
    chosen_fmt = None

    for fmt in preferred:
        for entry in sub_formats:
            if entry.get("ext") == fmt:
                chosen = entry
                chosen_fmt = fmt
                break
        if chosen:
            break

    if not chosen:
        chosen = sub_formats[0]
        chosen_fmt = chosen.get("ext", "unknown")

    sub_url = chosen["url"]
    with urllib.request.urlopen(sub_url) as response:
        raw_text = response.read().decode("utf-8")

    return raw_text, chosen_fmt

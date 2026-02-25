import argparse
import sys
import re

from downloader import fetch_subtitles, get_available_langs


def is_valid_youtube_url(url: str) -> bool:
    patterns = [
        r"^https?://(www\.)?youtube\.com/watch\?v=[\w-]+",
        r"^https?://youtu\.be/[\w-]+",
        r"^https?://(www\.)?youtube\.com/shorts/[\w-]+",
    ]
    return any(re.match(p, url) for p in patterns)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Download and format subtitles from a YouTube video.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
  python main.py https://youtu.be/dQw4w9WgXcQ --lang ru
  python main.py https://youtu.be/dQw4w9WgXcQ --output subtitles.txt
  python main.py https://youtu.be/dQw4w9WgXcQ --list-langs
        """,
    )

    parser.add_argument(
        "url",
        metavar="URL",
        help="YouTube video URL",
    )
    parser.add_argument(
        "--lang",
        metavar="LANG",
        default="en",
        help="subtitle language code (default: en)",
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        default=None,
        help="save output to a file instead of printing to stdout",
    )
    parser.add_argument(
        "--list-langs",
        action="store_true",
        help="list available subtitle languages and exit",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="skip text normalization and return raw subtitle text",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not is_valid_youtube_url(args.url):
        print(f"error: '{args.url}' does not look like a valid YouTube URL", file=sys.stderr)
        sys.exit(1)

    if args.list_langs:
        langs = get_available_langs(args.url)
        if langs["manual"]:
            print("Manual subtitles:    " + ", ".join(langs["manual"]))
        else:
            print("Manual subtitles:    (none)")
        if langs["automatic"]:
            print("Auto-generated:      " + ", ".join(langs["automatic"]))
        else:
            print("Auto-generated:      (none)")
        sys.exit(0)

    langs = get_available_langs(args.url)
    all_langs = set(langs["manual"]) | set(langs["automatic"])

    if args.lang not in all_langs:
        print(f"error: subtitles for language '{args.lang}' are not available", file=sys.stderr)
        if all_langs:
            manual_str = ", ".join(langs["manual"]) if langs["manual"] else "(none)"
            auto_str = ", ".join(langs["automatic"]) if langs["automatic"] else "(none)"
            print(f"  Manual subtitles:  {manual_str}", file=sys.stderr)
            print(f"  Auto-generated:    {auto_str}", file=sys.stderr)
        else:
            print("  No subtitles are available for this video.", file=sys.stderr)
        sys.exit(1)

    raw_text, fmt = fetch_subtitles(args.url, args.lang)
    print(raw_text)


if __name__ == "__main__":
    main()

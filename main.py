import argparse
import sys
import re


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

    print(f"URL:        {args.url}")
    print(f"Language:   {args.lang}")
    print(f"Output:     {args.output or 'stdout'}")
    print(f"List langs: {args.list_langs}")
    print(f"Clean text: {not args.no_clean}")


if __name__ == "__main__":
    main()

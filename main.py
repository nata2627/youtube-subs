import sys
import re

import click

from downloader import fetch_subtitles, get_available_langs
from parser import parse
from cleaner import clean
from output import write_output


def is_valid_youtube_url(url: str) -> bool:
    patterns = [
        r"^https?://(www\.)?youtube\.com/watch\?v=[\w-]+",
        r"^https?://youtu\.be/[\w-]+",
        r"^https?://(www\.)?youtube\.com/shorts/[\w-]+",
    ]
    return any(re.match(p, url) for p in patterns)


@click.command()
@click.argument("url")
@click.option("--lang", default="en", metavar="LANG", help="Subtitle language code (default: en)")
@click.option("--output", "-o", default=None, metavar="FILE", help="Save output to a file instead of printing to stdout")
@click.option("--list-langs", is_flag=True, help="List available subtitle languages and exit")
@click.option("--no-clean", is_flag=True, help="Skip text normalization and return raw subtitle text")
def main(url, lang, output, list_langs, no_clean):
    """Download and format subtitles from a YouTube video.

    \b
    Examples:
      python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
      python main.py https://youtu.be/dQw4w9WgXcQ --lang ru
      python main.py https://youtu.be/dQw4w9WgXcQ --output subtitles.txt
      python main.py https://youtu.be/dQw4w9WgXcQ --list-langs
    """
    if not is_valid_youtube_url(url):
        click.echo(f"error: '{url}' does not look like a valid YouTube URL", err=True)
        sys.exit(1)

    if list_langs:
        click.echo("[*] Fetching video metadata...", err=True)
        langs = get_available_langs(url)
        click.echo("[ok] Done", err=True)
        if langs["manual"]:
            click.echo("Manual subtitles:    " + ", ".join(langs["manual"]))
        else:
            click.echo("Manual subtitles:    (none)")
        if langs["automatic"]:
            click.echo("Auto-generated:      " + ", ".join(langs["automatic"]))
        else:
            click.echo("Auto-generated:      (none)")
        sys.exit(0)

    click.echo("[*] Fetching video metadata...", err=True)
    langs = get_available_langs(url)
    all_langs = set(langs["manual"]) | set(langs["automatic"])

    if lang not in all_langs:
        click.echo(f"error: subtitles for language '{lang}' are not available", err=True)
        if all_langs:
            manual_str = ", ".join(langs["manual"]) if langs["manual"] else "(none)"
            auto_str = ", ".join(langs["automatic"]) if langs["automatic"] else "(none)"
            click.echo(f"  Manual subtitles:  {manual_str}", err=True)
            click.echo(f"  Auto-generated:    {auto_str}", err=True)
        else:
            click.echo("  No subtitles are available for this video.", err=True)
        sys.exit(1)

    click.echo(f"[*] Downloading subtitles ({lang})...", err=True)
    raw_text, fmt = fetch_subtitles(url, lang)
    click.echo("[ok] Done", err=True)
    lines = parse(raw_text, fmt)
    if not no_clean:
        lines = clean(lines)

    if output:
        write_output(lines, output)
    else:
        click.echo("\n".join(lines))


if __name__ == "__main__":
    main()

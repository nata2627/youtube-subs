import sys

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from downloader import fetch_subtitles, get_available_langs, is_valid_youtube_url
from parser import parse
from cleaner import clean
from output import write_output, print_langs_table, print_subtitles

_err = Console(stderr=True)


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
        _err.print(f"[red]error:[/red] '{url}' does not look like a valid YouTube URL")
        sys.exit(1)

    if list_langs:
        with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=_err, transient=True) as progress:
            progress.add_task("Fetching video metadata...", total=None)
            langs = get_available_langs(url)
        print_langs_table(langs)
        sys.exit(0)

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=_err, transient=True) as progress:
        progress.add_task("Fetching video metadata...", total=None)
        langs = get_available_langs(url)

    all_langs = set(langs["manual"]) | set(langs["automatic"])

    if lang not in all_langs:
        _err.print(f"[red]error:[/red] subtitles for language '[bold]{lang}[/bold]' are not available")
        if all_langs:
            manual_str = ", ".join(langs["manual"]) if langs["manual"] else "(none)"
            auto_str = ", ".join(langs["automatic"]) if langs["automatic"] else "(none)"
            _err.print(f"  Manual subtitles:  {manual_str}")
            _err.print(f"  Auto-generated:    {auto_str}")
        else:
            _err.print("  No subtitles are available for this video.")
        sys.exit(1)

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=_err, transient=True) as progress:
        progress.add_task(f"Downloading subtitles ({lang})...", total=None)
        raw_text, fmt = fetch_subtitles(url, lang)

    lines = parse(raw_text, fmt)
    if not no_clean:
        lines = clean(lines)

    if output:
        write_output(lines, output)
    else:
        print_subtitles(lines, lang)


if __name__ == "__main__":
    main()

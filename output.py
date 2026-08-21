import os

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

_out = Console()


def write_output(lines: list[str], path: str) -> None:
    if os.path.exists(path):
        if not click.confirm(f"File '{path}' already exists. Overwrite?"):
            click.echo("Aborted.", err=True)
            raise SystemExit(0)

    ext = os.path.splitext(path)[1].lower()
    content = _format_content(lines, ext)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    click.echo(f"Saved to {path}")


def _format_content(lines: list[str], ext: str) -> str:
    if ext == ".md":
        body = "\n".join(lines)
        return f"# Subtitles\n\n```\n{body}\n```\n"
    return "\n".join(lines) + "\n"


def print_langs_table(langs: dict) -> None:
    table = Table(title="Available subtitles")
    table.add_column("Code", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    for code in langs["manual"]:
        table.add_row(code, "manual")
    for code in langs["automatic"]:
        table.add_row(code, "auto-generated")

    if not langs["manual"] and not langs["automatic"]:
        _out.print("No subtitles available for this video.")
    else:
        _out.print(table)


def print_subtitles(lines: list[str], lang: str) -> None:
    _out.print(Panel("\n".join(lines), title=f"Subtitles [{lang}]"))

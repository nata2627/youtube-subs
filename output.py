import os

import click


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

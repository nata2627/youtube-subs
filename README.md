# yt-subtitle-dl

Download and format subtitles from YouTube videos via the command line.

## Requirements

- Python 3.10+

## Installation

```bash
git clone https://github.com/your-username/yt-subtitle-dl.git
cd yt-subtitle-dl
pip install -r requirements.txt
```

## Usage

```
python main.py URL [--lang LANG] [--output FILE] [--list-langs] [--no-clean]
```

## Flags

| Flag | Description |
|------|-------------|
| `URL` | YouTube video URL (required) |
| `--lang LANG` | Subtitle language code, e.g. `en`, `ru`, `de` (default: `en`) |
| `--output FILE`, `-o FILE` | Save output to a file instead of printing to stdout |
| `--list-langs` | Print available subtitle languages and exit |
| `--no-clean` | Skip text normalization, return raw subtitle text |

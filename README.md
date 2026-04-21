# Goodreads Quote Scraper

A Python web scraper that extracts quotes from Goodreads and saves them to CSV format.

## Features

- Scrapes quotes from Goodreads author pages
- Extracts quote text, author, and tags
- Exports to CSV format
- Uses Playwright for dynamic content loading

## Requirements

- Python 3.12+
- uv (recommended) or pip

## Installation

### Using UV (recommended)

```bash
uv sync
```

### Using pip

```bash
pip install -r requirements.txt
```

## Usage

```bash
uv run main.py
```

Or with Python directly:

```bash
python main.py
```

## Output

Creates `quotes.csv` with the following columns:

- `quote`: The quote text
- `author`: The quote author
- `tags`: Comma-separated tags

## Project Structure

```
.
├── main.py           # Main scraper script
├── pyproject.toml   # Project configuration
├── README.md        # This file
└── .gitignore       # Git ignore patterns
```

## License

MIT License - see [LICENSE](LICENSE) for details.
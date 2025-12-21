# Goodreads Quote Scraper

Simple web scraper that extracts quotes from Goodreads.

## Requirements
- Python 3.x
- pandas
- beautifulsoup4
- requests

## Installation

### Using UV (recommended)
```bash
uv sync
uv run main.py
```

### Using pip
```bash
pip install -r requirements.txt
python main.py
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
Creates `quotes.csv` with columns: quote, author, tags
```

## 5. **Create requirements.txt**
```
pandas
beautifulsoup4
requests
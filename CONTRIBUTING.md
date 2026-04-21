# Contributing to Goodreads Quote Scraper

Thank you for your interest in contributing!

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and relevant package versions

### Suggesting Features

1. Open a new issue labeled "feature request"
2. Describe the proposed feature
3. Explain why this would be useful

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `pytest`
5. Push to your fork and submit a pull request
6. Ensure CI passes

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/book-quote-scraper.git
cd book-quote-scraper

# Install dependencies
uv sync

# Install dev dependencies
uv sync --group dev

# Run tests
pytest

# Format code
black .

# Lint code
flake8 .
```

## Code Style

- Follow PEP 8
- Use Black for formatting
- Use type hints where appropriate
- Write docstrings for functions and classes
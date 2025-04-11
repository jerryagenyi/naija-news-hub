# News Scraper

A flexible news scraper that automatically extracts articles from any news website when provided with a base URL.

## Features

- Automatically detects and extracts news articles from a website
- Extracts article title, content, author, publication date, and categories
- Simple command-line interface
- Supports saving articles to various formats (JSON, CSV)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/jerryagenyi/scraper-2.git
   cd scraper-2
   ```

2. Create a virtual environment and activate it:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Basic usage:
```
python -m scraper.main --url https://example-news-site.com
```

For more options:
```
python -m scraper.main --help
```

## License

MIT

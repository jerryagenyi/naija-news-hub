# Naija News Hub

A robust, adaptable, and scalable system for aggregating news content from a diverse range of Nigerian online news sources, enabling data-driven research and analysis through advanced web scraping and LLM integration.

Naija News Hub is a news aggregation platform that collects Nigerian news articles for research and analysis. The scraped articles will be vectorized and used to train an LLM for a chat interface. This is not a public-facing news browsing platform, but rather a data collection and analysis tool for research purposes.

## Features

- Automatically discovers and extracts news articles from websites
- Extracts article title, content, author, publication date, and categories
- Provides a RESTful API for accessing the data
- Supports advanced research capabilities through LLM integration
- Includes comprehensive monitoring and error handling
- Offers a user-friendly interface for managing the system

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/jerryagenyi/naija-news-hub.git
   cd naija-news-hub
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

4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```
   python main.py init
   ```

## Usage

### Running the API server

```
python main.py api --host 0.0.0.0 --port 8000
```

### Running the scraper

To scrape a specific website:
```
python main.py scrape --website-id 1
```

To scrape all active websites:
```
python main.py scrape --all
```

### Using the utility scripts

#### Adding websites to the database

To add Blueprint.ng and Daily Trust to the database:
```
python scripts/add_websites.py
```

#### Triggering scraping via the API

To trigger scraping for websites via the API:
```
python scripts/trigger_scraping.py
```
This script provides an interactive interface to scrape specific websites or all websites.

### Command-line help

```
python main.py --help
```

## Development Guidelines

### File Relationship Rules

This project follows strict file relationship rules to maintain integrity across documentation and code. Before making changes to any file, please review the [File Relationship Rules](docs/dev/file-relationship-rules.md) document to understand which related files might need updates.

### Project Journey

To understand the evolution of this project and the decisions made along the way, check out our [Project Journey](docs/pm/project-journey.md) document.

## License

MIT

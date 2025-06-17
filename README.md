# Goods Parser

A simple Python tool for parsing and extracting product data from various e-commerce websites. The script leverages `requests`, `BeautifulSoup`, and `sqlite3` to fetch and store structured data from HTML pages.

## Features

- Parses product listings from supported websites
- Stores data into a local SQLite database
- Supports CLI usage
- Logs and handles duplicates during parsing

## Requirements

- Python 3.8+
- SQLite3
- BeautifulSoup4
- Requests

## Installation

1. Clone the repository:

```bash
git clone https://github.com/alikkosenko/goods_parser.git
cd goods_parser
```

    Create and activate a virtual environment (optional):
```bash
python3 -m venv venv
source venv/bin/activate
```

    Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 GCrawler.py
```

You can edit GCrawler.py to customize the target URLs and parsing logic according to your needs.

## Database

The script stores results in an SQLite database file (products.db). You can inspect it using tools like sqlite3 CLI or a GUI like DB Browser for SQLite.

## License

MIT License. See LICENSE for details.


---

### ✅ `requirements.txt`

```txt
beautifulsoup4==4.12.3
requests==2.31.0
selenium==4.20.0
undetected-chromedriver==3.5.5
pyTelegramBotAPI==4.16.1

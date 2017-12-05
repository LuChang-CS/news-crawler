# news-crawler

A news crawler for BBC News, Reuters and New York Times.

## Requirements

- python3
- configobj: `pip install configobj`
- dateutil: `pip install python-dateutil`
- requests: `pip install requests`
- bs4: `pip install bs4`
- goose3: `pip install goose3`

## Architecture

- xxx_crawler: the executive file to crawl news.
- xxx.cfg: configurations for the crawler, including api, time range and storage path etc.
- xxx_link.py: fetch download links.
- xxx_article: extract content and some meta data of one news article.

## Usage

### BBC News

```bash
python bbc_crawler.py
```

### Reuters

```bash
python reuters_crawler.py
```

### New York Times

```bash
python nytimes_crawler.py
```

## Configuration

Modify `reuters.cfg`, `nytimes.cfg` and `bbc.cfg` in settings folder, the main configuration items may be `start_date`, `end_date` and `path`.

## Notes

If other news sources need to be added, just add files as the architecture, extend the basic class in each folder. Some methods may need to be rewrote.

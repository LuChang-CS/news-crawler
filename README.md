# news-crawler

A news crawler for BBC News, Reuters and New York Times.

## Update and Clarification (2021/10/03)

- For BBC: It is a news collection from BBC front pages [https://www.bbc.com/news](https://www.bbc.com/news), starting from 2015/07/01/. This archive is collected by [@dracos](https://github.com/dracos). Please refer to his website: [https://dracos.co.uk/made/bbc-news-archive/archive.php](https://dracos.co.uk/made/bbc-news-archive/archive.php).
- For Reuters, they have disabled their original archive website. The new website [https://www.reuters.com/news/archive](https://www.reuters.com/news/archive) has only a limited number of historical articles (starting from 2020/03/08), so I did not update codes for Reuters anymore. But I still keep the codes for Reuters as an example, in case that you want to implement your own codes for Reuters.

## Requirements

- python3
- configobj
- dateutil
- requests
- bs4
- goose3
```bash
pip install -r requirements.txt
```

## Architecture

- xxx_crawler: the executive file to crawl news.
- xxx.cfg: configurations for the crawler, including api, time range and storage path etc.
- xxx_link.py: fetch download links.
- xxx_article: extract content and some meta data of one news article.

## Usage

### BBC News

```bash
python bbc_crawler.py settings/bbc.cfg
```

### Reuters

```bash
python reuters_crawler.py reuters.cfg
```

### New York Times

```bash
python nytimes_crawler.py nytimes.cfg
```

## Configuration

Modify `reuters.cfg`, `nytimes.cfg` and `bbc.cfg` in settings folder, the main configuration items may be `start_date`, `end_date` and `path`.

## Notes

If other news sources need to be added, just add files as the architecture, extend the basic class in each folder. Some methods may need to be rewrote.

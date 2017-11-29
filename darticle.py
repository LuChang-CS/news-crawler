import os.path
import json
from datetime import timedelta

from network import NetworkFetcher


class ArticleFetcher:

    def __init__(self, config):
        self.download_link_fetcher = None
        self.html_fetcher = NetworkFetcher()
        self.path = config.path

        self._mkdir(self.path,
                    config.start_date,
                    config.end_date,
                    config.step)

    def _mkdir(self, path, start_date, end_date, step):
        step = timedelta(days=1)
        current_date = start_date
        existed_years = dict()
        while current_date < end_date:
            year = current_date.year
            month = current_date.month
            day = current_date.day

            year_path = os.path.join(path, str(year))
            month_path = os.path.join(year_path, str(month))
            day_path = os.path.join(month_path, day)

            if year not in existed_years.keys():
                existed_years[year] = dict()
                os.mkdir(year_path)

            year_content = existed_years[year]
            if month not in year_content.keys():
                year_content[month] = True
                os.mkdir(month)

            os.mkdir(day_path)
            current_date += step

    def _html_to_infomation(self, html):
        return {}

    def _extract_information(self, link):
        html = self.html_fetcher.fetch(link)
        return self._html_to_infomation(html)

    def _get_storage_path(self, path, date):
        return os.path.join(path, str(date.year), str(date.month), str(date.day))

    def _lazy_storage(self, storage_path, links):
        titles_path = os.path.join(storage_path, 'titles')
        with open(titles_path, mode='w', encoding='utf-8') as titles_file:
            articles = list()
            titles = list()
            for link in links:
                article = self._extract_information(link)
                titles.append(article['title'] + '\n')
                articles.append(article)

            articles_path = os.path.join(storage_path, 'articles')
            with open(articles_path, mode='w', encoding='utf-8') as articles_file:
                json.dump({
                    'number': len(articles),
                    'articles': articles
                }, articles_file)
            titles_file.write(titles)

    def _non_lazy_storage(self, storage_path, links):
        titles_path = os.path.join(storage_path, 'titles')
        with open(titles_path, mode='w', encoding='utf-8') as titles_file:
            for article_index, link in enumerate(links):
                article = self._extract_information(link)
                titles_file.write(article['title'] + '\n')

                article_path = os.path.join(storage_path, str(article_index))
                with open(article_path, mode='w', encoding='utf-8') as article_file:
                    json.dump(article, article_file)

    def fetch(self, lazy_storage=True):
        while True:
            api_url, date = self.download_link_fetcher.next()
            if api_url is None:
                break
            storage_path = self._get_storage_path(self.path, date)
            links = self.download_link_fetcher.fetch(api_url)
            if lazy_storage:
                self._lazy_storage(storage_path, links)
            else:
                self._non_lazy_storage(storage_path, links)

import sys
import os.path
import json
import time
from datetime import timedelta

from network.network import NetworkFetcher


class ArticleFetcher:

    RETRY = 5

    def __init__(self, config):
        self.config = config
        self.download_link_fetcher = None
        self.html_fetcher = NetworkFetcher()
        self.path = config.path

        self.total_date = 0

        self._mkdir(self.path,
                    config.start_date,
                    config.end_date,
                    config.step)

    def _mkdir(self, path, start_date, end_date, step):
        if os.path.isdir(path):
            # current_date = start_date
            # while current_date < end_date:
            #     current_date += step
            #     self.total_date += 1
            # return
            pass
        else:
            os.makedirs(path)
        current_date = start_date
        existed_years = dict()
        while current_date < end_date:
            year = current_date.year
            month = current_date.month
            day = current_date.day

            year_path = os.path.join(path, str(year))
            month_path = os.path.join(year_path, str(month))
            day_path = os.path.join(month_path, str(day))

            if year not in existed_years.keys():
                existed_years[year] = dict()
                if not os.path.isdir(year_path):
                    os.mkdir(year_path)

            if (step.months > 0) or (step.days > 0):
                year_content = existed_years[year]
                if month not in year_content.keys():
                    year_content[month] = True
                    if not os.path.isdir(month_path):
                        os.mkdir(month_path)

            if step.days > 0:
                if not os.path.isdir(day_path):
                    os.mkdir(day_path)
            current_date += step

            self.total_date += 1

    def _html_to_infomation(self, html, link, date):
        return {}

    def _extract_information(self, link, date):
        html = self.html_fetcher.fetch(link)
        if html is None:
            for _ in range(0, self.RETRY):
                html = self.html_fetcher.fetch(link)
                if html is not None:
                    break
        if html is None:
            print('article ', link, 'failed')
            return None
        return self._html_to_infomation(html, link, date)

    def _get_storage_path(self, path, date):
        return os.path.join(path, str(date.year), str(date.month), str(date.day))

    def _lazy_storage(self, storage_path, links, date):
        total_links = len(links)
        current_link = 1

        titles_path = os.path.join(storage_path, 'titles')
        with open(titles_path, mode='w', encoding='utf-8') as titles_file:
            articles = list()
            titles = list()
            for link in links:
                print('>>> {c} in {t} articles\r'.format(c=current_link, t=total_links), end='')
                current_link += 1

                article = self._extract_information(link, date)
                if article is not None:
                    titles.append(article['title'] + '\n')
                    articles.append(article)

            articles_path = os.path.join(storage_path, 'articles')
            with open(articles_path, mode='w', encoding='utf-8') as articles_file:
                json.dump({
                    'expected_number': len(links),
                    'number': len(articles),
                    'articles': articles
                }, articles_file, indent=4)
            titles_file.writelines(titles)

    def _non_lazy_storage(self, storage_path, links, date):
        total_links = len(links)
        current_link = 1

        titles_path = os.path.join(storage_path, 'titles')
        with open(titles_path, mode='w', encoding='utf-8') as titles_file:
            for article_index, link in enumerate(links):
                print('{c} in {t} articles\r'.format(c=current_link, t=total_links), end='')
                current_link += 1

                article = self._extract_information(link, date)
                if article is not None:
                    titles_file.write(article['title'] + '\n')

                    article_path = os.path.join(storage_path, str(article_index))
                    with open(article_path, mode='w', encoding='utf-8') as article_file:
                        json.dump(article, article_file, indent=4)

    def fetch(self, lazy_storage=True):
        current_date = 1
        while True:
            api_url, date = self.download_link_fetcher.next()
            if api_url is None:
                break
            print(date.strftime('%Y-%m-%d'),
                  '{c} in {t} dates                  '.format(c=current_date, t=self.total_date))

            storage_path = self._get_storage_path(self.path, date)
            links = self.download_link_fetcher.fetch(api_url)
            if lazy_storage:
                self._lazy_storage(storage_path, links, date)
            else:
                self._non_lazy_storage(storage_path, links, date)

            time.sleep(self.config.sleep)

            print(date.strftime('%Y-%m-%d'),
                  'date {c} finished                 '.format(c=current_date))
            current_date += 1

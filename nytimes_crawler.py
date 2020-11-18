import sys
import os.path
import json

from dateutil.relativedelta import relativedelta

from settings.dataset_conf import DatasetConfiguration
from article.nytimes_article import NytimeArticleFetcher


def parse_nytimes(fetcher):
    config = fetcher.config
    current_date = config.start_date
    while current_date < config.end_date:
        storage_path = fetcher._get_storage_path(config.path, current_date)
        articles_path = os.path.join(storage_path, 'articles')
        with open(articles_path, encoding='utf-8') as articles_file:
            articles = json.load(articles_file)
            day_articles = list()
            day_titles = list()
            for _ in range(0, 31):
                day_articles.append([])
                day_titles.append([])
            for article in articles['articles']:
                day = int(article['published_date'][-2:])
                day_articles[day - 1].append(article)
                day_titles[day - 1].append(article['title'] + '\n')

            day_step = relativedelta(days=1)
            month_start_date = current_date
            month_end_date = month_start_date + relativedelta(months=1)
            month_end_date.replace(day=1)
            if month_end_date > config.end_date:
                month_end_date = config.end_date

            month_current_date = month_start_date
            while month_current_date < month_end_date:
                day = month_current_date.day
                day_path = os.path.join(storage_path, str(day))
                if not os.path.isdir(day_path):
                    os.mkdir(day_path)

                day_titles_path = os.path.join(day_path, 'titles')
                with open(day_titles_path, mode='w', encoding='utf-8') as day_titles_file:
                    day_titles_file.writelines(day_titles[day - 1])
                day_articles_path = os.path.join(day_path, 'articles')
                with open(day_articles_path, mode='w', encoding='utf-8') as day_articles_file:
                    json.dump({
                        'number': len(day_articles[day - 1]),
                        'articles': day_articles[day - 1]
                    }, day_articles_file, indent=4)

                month_current_date += day_step

        current_date += config.step

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('please input configuration path')
        exit()
    config = DatasetConfiguration()
    config.load(sys.argv[1])

    nytime_article_fetcher = NytimeArticleFetcher(config)
    nytime_article_fetcher.fetch()

    parse_nytimes(nytime_article_fetcher)

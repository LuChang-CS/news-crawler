import sys

from settings.dataset_conf import DatasetConfiguration
from article.reuters_article import ReutersArticleFetcher


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('please input configuration path')
        exit()
    config = DatasetConfiguration()
    config.load(sys.argv[1])

    reuters_article_fetcher = ReutersArticleFetcher(config)
    reuters_article_fetcher.fetch()

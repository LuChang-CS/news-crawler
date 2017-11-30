from settings.dataset_conf import DatasetConfiguration
from article.reuters_article import ReutersArticleFetcher


if __name__ == '__main__':
    config = DatasetConfiguration()
    config.load('./settings/reuters.cfg')

    reuters_article_fetcher = ReutersArticleFetcher(config)
    reuters_article_fetcher.fetch()

from settings.dataset_conf import DatasetConfiguration
from article.bbc_article import BBCArticleFetcher


if __name__ == '__main__':
    config = DatasetConfiguration()
    config.load('./settings/bbc.cfg')

    bbc_article_fetcher = BBCArticleFetcher(config)
    bbc_article_fetcher.fetch()

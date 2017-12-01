from settings.dataset_conf import DatasetConfiguration
from link.nytimes_link import NytimesLinkFetcher


if __name__ == '__main__':
    config = DatasetConfiguration()
    config.load('./settings/nytimes.cfg')

    nytimes_link_fetcher = NytimesLinkFetcher(config)
    api_urls, date = nytimes_link_fetcher.next()
    links = nytimes_link_fetcher.fetch(api_urls)
    print(links)

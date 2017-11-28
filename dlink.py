from bs4 import BeautifulSoup

from network import NetworkFetcher

class DownloadLinkFetcher:

    BBC_FILTERS = [
        ['programmes', 21, 31],
        ['correspondents', 26, 40],
        ['iplayer', 21, 28],
        ['radio', 21, 26],
        ['live', 27, 31],
        ['m', 7, 8]
    ]

    def __init__(self):
        self.html_fetcher = NetworkFetcher()

    def _format_link(self, link):
        hash_index = link.find('#')
        if hash_index != -1:
            link = link[:hash_index]
        if link[-1] == '/':
            link = link[:-1]
        return link

    def _link_filter(self, link, filters):
        if not link[-1].isdigit():
            return False
        for filter_ in filters:
            if link[filter_[1]:filter_[2]] == filter_[0]:
                return False
        return True

    def bbc(self, api_url):
        html = self.html_fetcher.fetch(api_url)
        soup = BeautifulSoup(html, 'lxml')

        links = list()
        # news links are the hrefs of a
        elements = soup.table.find_all('a')
        for element in elements:
            # this a is not news link
            if element.get('rel', None) is not None:
                continue
            link = self._format_link(element['href'])
            if self._link_filter(link, self.BBC_FILTERS):
                links.append(link)

        return list(set(links))

# test
if __name__ == '__main__':
    download_link_fetcher = DownloadLinkFetcher()
    links = download_link_fetcher.bbc('http://dracos.co.uk/made/bbc-news-archive/2017/11/27/')
    print(links)

from bs4 import BeautifulSoup

from .dlink import DownloadLinkFetcher


class NytimesLinkFetcher(DownloadLinkFetcher):
    ''' If you use http://spiderbites.nytimes.com/, you need to rewrite some methods.
        If you use nytimes api with key, it's the same with other corpus.
        This class uses the first website to crawl ntyime articles.
    '''

    def __init__(self, config):
        super(NytimesLinkFetcher, self).__init__(config)
        self.current_year = None
        self.current_api_url = None

        self.month_links = []

        self.start_date = config.start_date_
        self.current_date = config.start_date_
        self.end_date = config.end_date_

    def _fetch_year_links(self):
        print('fetching new years links')
        html = self.html_fetcher.fetch(self.current_api_url)
        soup = BeautifulSoup(html, 'lxml')
        month_elements = soup.find_all('div', class_='articlesMonth')
        for month_element in month_elements:
            self.month_links.append(
                [(self.current_api_url[:30] + a['href']) for a in month_element.find_all('a')])

    def _next_api(self, base_url, current_date):
        year = current_date.year
        if year == self.current_year:
            return self.month_links[current_date.month - 1]
        self.current_api_url = base_url.format(year=year)
        self._fetch_year_links()
        self.current_year = year
        return self.month_links[current_date.month - 1]

    def next(self):
        if self.current_date >= self.end_date:
            return None, None
        api_url = self._next_api(self.base_api_url, self.current_date)
        date = self.current_date
        self.current_date += self.step
        return api_url, date

    def _html_to_links(self, html):
        soup = BeautifulSoup(html, 'lxml')

        links = list()
        headlines_element = soup.find(id='headlines')
        elements = headlines_element.find_all('li')
        for element in elements:
            links.append((element.a)['href'])

        return list(set(links))

    def fetch(self, api_url):
        print('fetching download links...')
        links = list()
        for url in api_url:
            html = self.html_fetcher.fetch(url)
            links += self._html_to_links(html)
        return links

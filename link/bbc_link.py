from bs4 import BeautifulSoup

from .dlink import DownloadLinkFetcher



class BBCLinkFetcher(DownloadLinkFetcher):

    BBC_FILTERS = [
        ['programmes', 21, 31],
        ['correspondents', 26, 40],
        ['iplayer', 21, 28],
        ['radio', 21, 26],
        ['live', 27, 31],
        ['m', 7, 8]
    ]

    def _next_api(self, base_url, current_date):
        year = current_date.year
        month = current_date.month
        day = current_date.day
        api_url = base_url.format(year=year, month=month, day=day)
        return api_url

    def _html_to_links(self, html):
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

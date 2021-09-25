from bs4 import BeautifulSoup

from .dlink import DownloadLinkFetcher


class NytimesLinkFetcher(DownloadLinkFetcher):

    def _next_api(self, base_url, current_date):
        year = current_date.year
        month = current_date.month
        day = current_date.day
        api_url = base_url.format(year=year, month=month, day=day)
        return api_url

    def _html_to_links(self, html):
        soup = BeautifulSoup(html, 'lxml')

        links = list()
        ul_element = soup.find('main').find('ul')
        elements = ul_element.find_all('a')
        for a in elements:
            links.append(a['href'])

        return list(set(links))

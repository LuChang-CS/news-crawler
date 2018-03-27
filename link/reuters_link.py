from bs4 import BeautifulSoup

from .dlink import DownloadLinkFetcher



class ReutersLinkFetcher(DownloadLinkFetcher):

    def _next_api(self, base_url, current_date):
        year = current_date.year
        month = current_date.month
        day = current_date.day
        api_url = base_url.format(year=year, month=month, day=day)
        return api_url

    def _html_to_links(self, html):
        soup = BeautifulSoup(html, 'lxml')

        links = list()
        module_element = soup.find('div', class_='module')
        elements = module_element.find_all('div', class_='headlineMed')
        for element in elements:
            links.append((element.a)['href'].replace('UK.reuters.com', 'www.reuters.com'))

        return list(set(links))

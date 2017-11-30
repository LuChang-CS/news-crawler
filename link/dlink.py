from network.network import NetworkFetcher

class DownloadLinkFetcher:

    def __init__(self, config):
        self.base_api_url = config.base_api_url

        self.start_date = config.start_date
        self.current_date = config.start_date
        self.end_date = config.end_date
        self.step_unit = config.step_unit
        self.step = config.step

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

    def _html_to_links(self, html):
        return []

    def _next_api(self, base_api_url, current_date):
        return ''

    def next(self):
        if self.current_date >= self.end_date:
            return None, None
        api_url = self._next_api(self.base_api_url, self.current_date)
        date = self.current_date
        self.current_date += self.step
        return api_url, date

    def fetch(self, api_url):
        html = self.html_fetcher.fetch(api_url)
        links = self._html_to_links(html)
        return links

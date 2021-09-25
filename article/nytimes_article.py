import os

from bs4 import BeautifulSoup
from goose3 import Goose
from dateutil.relativedelta import relativedelta

from network.network import NetworkFetcher
from .darticle import ArticleFetcher
from link.nytimes_link import NytimesLinkFetcher


class NytimeArticleFetcher(ArticleFetcher):

    def __init__(self, config):
        super(NytimeArticleFetcher, self).__init__(config)
        self.config = config
        self.download_link_fetcher = NytimesLinkFetcher(config)

    def _extract_title(self, soup):
        if soup.title is not None:
            return soup.title.get_text()

    def _extract_published_date(self, soup):
        publish_element = soup.find('meta', property='article:published_time')
        if publish_element is not None:
            date = publish_element['content']
            return date

    def _extract_authors(self, soup):
        authors_element = soup.find('meta', property='article:author')
        if authors_element is not None:
            return authors_element['content']

    def _extract_description(self, soup):
        description_element = soup.find('meta', {'name': 'description'})
        if description_element is not None:
            return description_element['content']

    def _extract_section(self, soup):
        section_element = soup.find('meta', property='article:section')
        if section_element is not None:
            return section_element['content']

    def _extract_content(self, html):
        g = Goose({'enable_image_fetching': False})
        article = g.extract(raw_html=html)
        return article.cleaned_text

    def _html_to_infomation(self, html, link, date):
        soup = BeautifulSoup(html, 'html5lib')
        head = soup

        try:
            title = self._extract_title(head)
            published_date = self._extract_published_date(head)
            authors = self._extract_authors(head)
            description = self._extract_description(head)
            section = self._extract_section(head)
            content = self._extract_content(html)
        except Exception as err:
            return None

        return {
            'title': title,
            'published_date': published_date,
            'authors': authors,
            'description': description,
            'section': section,
            'content': content,
            'link': link
        }

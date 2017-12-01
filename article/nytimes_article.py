import os

from bs4 import BeautifulSoup
from goose3 import Goose

from .darticle import ArticleFetcher
from link.nytimes_link import NytimesLinkFetcher


class NytimeArticleFetcher(ArticleFetcher):

    def __init__(self, config):
        super(NytimeArticleFetcher, self).__init__(config)
        self.download_link_fetcher = NytimesLinkFetcher(config)

    def _get_storage_path(self, path, date):
        return os.path.join(path, str(date.year), str(date.month))

    def _extract_title(self, soup):
        return soup.title.get_text()

    def _extract_published_date(self, soup):
        publish_element = soup.find('meta', name='ptime')
        date = publish_element['content']
        return '-'.join([date[:4], date[4:6], date[6:8]])

    def _extract_authors(self, soup):
        authors_element = soup.find('meta', name='author')
        return authors_element['content']

    def _extract_description(self, soup):
        description_element = soup.find('meta', name='description')
        return description_element['content']

    def _extract_section(self, soup):
        section_element = soup.find('meta', property='article:section')
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
            published_date = self._extract_published_date(date)
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

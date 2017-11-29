import json

from bs4 import BeautifulSoup

from darticle import ArticleFetcher
from bbc_link import BBCLinkFetcher

class BBCArticleFetcher(ArticleFetcher):

    def __init__(self, config):
        super().__init__(self, config)
        self.download_link_fetcher = BBCLinkFetcher(config)

    def _extract_title(self, soup):
        return soup.title

    def _extract_published_date(self, soup):
        meta_script = soup.script
        meta_info = json.loads(meta_script.get_text().strip())
        return meta_info['datePublished']

    def _extract_authors(self, soup):
        authors_elements = soup.find_all('meta', property='article:author')
        return [authors_element['content'] for authors_element in authors_elements]

    def _extract_description(self, soup):
        description_element = soup.find('meta', property='og:description')
        return description_element['content']

    def _extract_section(self, soup):
        section_element = soup.find('meta', property='article:section')
        return section_element['content']

    def _extract_content(self, soup):
        article_element = soup.find('div', property='articleBody')
        figure_elements = article_element.find_all('figure')
        for figure_element in figure_elements:
            figure_element.extract()

        return article_element.get_text()

    def _html_to_infomation(self, html):
        soup = BeautifulSoup(html, 'lxml')
        head = soup.head

        title = self._extract_title(head)
        published_date = self._extract_published_date(head)
        authors = self._extract_authors(head)
        description = self._extract_description(head)
        section = self._extract_section(head)
        content = self._extract_content(soup)

        return {
            'title': title,
            'published_date': published_date,
            'authors': authors,
            'description': description,
            'section': section,
            'content': content
        }

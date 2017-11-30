import json

from bs4 import BeautifulSoup
from goose3 import Goose

from darticle import ArticleFetcher
from bbc_link import BBCLinkFetcher


class BBCArticleFetcher(ArticleFetcher):

    def __init__(self, config):
        super(BBCArticleFetcher, self).__init__(config)
        self.download_link_fetcher = BBCLinkFetcher(config)

    def _extract_title(self, soup):
        return soup.title.get_text()

    def _extract_published_date(self, soup, link):
        published_date_element = soup.find('meta', property='rnews:datePublished')
        if published_date_element is not None:
            return published_date_element['content']
        meta_script = soup.script
        script_text = meta_script.get_text().strip().replace('\\n', '')
        meta_info = json.loads(script_text, encoding='utf-8')
        published_date = meta_info.get('datePublished', None)
        if published_date is None:
            video = meta_info.get('video', None)
            if video is not None:
                published_date = video['uploadDate']

        return published_date

    def _extract_authors(self, soup):
        authors_elements = soup.find_all('meta', property='article:author')
        return [authors_element['content'] for authors_element in authors_elements]

    def _extract_description(self, soup):
        description_element = soup.find('meta', property='og:description')
        return description_element['content']

    def _extract_section(self, soup):
        section_element = soup.find('meta', property='article:section')
        return section_element['content']

    def _extract_content(self, html):
        g = Goose({'enable_image_fetching': False})
        article = g.extract(raw_html=html)
        return article.cleaned_text

    def _html_to_infomation(self, html, link):
        soup = BeautifulSoup(html, 'lxml')
        head = soup.head

        try:
            title = self._extract_title(head)
            published_date = self._extract_published_date(head, link)
            authors = self._extract_authors(head)
            description = self._extract_description(head)
            section = self._extract_section(head)
            content = self._extract_content(html)
        except Exception:
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

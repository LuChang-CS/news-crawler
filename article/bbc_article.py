import json

from bs4 import BeautifulSoup
from goose3 import Goose
from goose3.extractors.content import ContentExtractor

from .darticle import ArticleFetcher
from link.bbc_link import BBCLinkFetcher


eps = 1e-6
f1 = ContentExtractor.calculate_best_node
f2 = ContentExtractor.post_cleanup


def post_cleanup(ce_inst):
    """\
    remove any divs that looks like non-content,
    clusters of links, or paras with no gusto
    """
    parse_tags = ['p']
    if ce_inst.config.parse_lists:
        parse_tags.extend(['ul', 'ol'])
    if ce_inst.config.parse_headers:
        parse_tags.extend(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    target_node = ce_inst.article.top_node
    node = ce_inst.add_siblings(target_node)
    for elm in ce_inst.parser.getChildren(node):
        e_tag = ce_inst.parser.getTag(elm)
        if e_tag not in parse_tags:
            if ce_inst.is_highlink_density(elm) or ce_inst.is_table_and_no_para_exist(elm):
                ce_inst.parser.remove(elm)
    return node


def calculate_best_node(ce_inst, doc):
    top_node = None
    nodes_to_check = ce_inst.nodes_to_check(doc)

    starting_boost = float(1.0)
    cnt = 0
    i = 0
    parent_nodes = []
    nodes_with_text = []

    for node in nodes_to_check:
        text_node = ce_inst.parser.getText(node)
        word_stats = ce_inst.stopwords_class(language=ce_inst.get_language()).get_stopword_count(text_node)
        high_link_density = ce_inst.is_highlink_density(node)
        if word_stats.get_stopword_count() > 2 and not high_link_density:
            nodes_with_text.append(node)

    nodes_number = len(nodes_with_text)
    negative_scoring = 0
    bottom_negativescore_nodes = float(nodes_number) * 0.25

    for node in nodes_with_text:
        boost_score = float(0)
        # boost
        if ce_inst.is_boostable(node):
            if cnt >= 0:
                boost_score = float((1.0 / starting_boost) * 50)
                starting_boost += 1
        # nodes_number
        if nodes_number > 15:
            if (nodes_number - i) <= bottom_negativescore_nodes:
                booster = float(bottom_negativescore_nodes - (nodes_number - i))
                boost_score = float(-pow(booster, float(2)))
                negscore = abs(boost_score) + negative_scoring
                if negscore > 40:
                    boost_score = float(5)

        text_node = ce_inst.parser.getText(node)
        word_stats = ce_inst.stopwords_class(language=ce_inst.get_language()).get_stopword_count(text_node)
        upscore = int(word_stats.get_stopword_count() + boost_score)

        # parent node
        parent_node = ce_inst.parser.getParent(node)
        ce_inst.update_score(parent_node, upscore)
        ce_inst.update_node_count(parent_node, 1)

        if parent_node not in parent_nodes:
            parent_nodes.append(parent_node)

        # parentparent node
        parent_parent_node = ce_inst.parser.getParent(parent_node)
        if parent_parent_node is not None:
            ce_inst.update_node_count(parent_parent_node, 1)
            ce_inst.update_score(parent_parent_node, upscore - eps)
            if parent_parent_node not in parent_nodes:
                parent_nodes.append(parent_parent_node)

        # parentparentparent node
        parent_parent_parent_node = ce_inst.parser.getParent(parent_parent_node)
        if parent_parent_parent_node is not None:
            ce_inst.update_node_count(parent_parent_parent_node, 1)
            ce_inst.update_score(parent_parent_parent_node, upscore - 2 * eps)
            if parent_parent_parent_node not in parent_nodes:
                parent_nodes.append(parent_parent_parent_node)
        cnt += 1
        i += 1

    top_node_score = 0
    for itm in parent_nodes:
        score = ce_inst.get_score(itm)

        if score > top_node_score:
            top_node = itm
            top_node_score = score

        if top_node is None:
            top_node = itm

    return top_node


class BBCArticleFetcher(ArticleFetcher):

    def __init__(self, config):
        super(BBCArticleFetcher, self).__init__(config)
        self.download_link_fetcher = BBCLinkFetcher(config)

    def _extract_title(self, soup):
        if soup.title is not None:
            return soup.title.get_text()

    def _extract_published_date(self, date):
        return date.strftime('%Y-%m-%d')

    def _extract_authors(self, soup):
        authors_elements = soup.find_all('meta', property='article:author')
        if authors_elements is not None:
            return [authors_element['content'] for authors_element in authors_elements]

    def _extract_description(self, soup):
        description_element = soup.find('meta', property='og:description')
        if description_element is not None:
            return description_element['content']

    def _extract_section(self, soup):
        section_element = soup.find('meta', property='article:section')
        if section_element is not None:
            return section_element['content']

    def _extract_content(self, html):
        ContentExtractor.calculate_best_node = calculate_best_node
        ContentExtractor.post_cleanup = post_cleanup
        g = Goose({'enable_image_fetching': False})
        article = g.extract(raw_html=html)
        ContentExtractor.calculate_best_node = f1
        ContentExtractor.post_cleanup = f2
        return article.cleaned_text

    def _html_to_infomation(self, html, link, date):
        soup = BeautifulSoup(html, 'lxml')
        head = soup.head

        try:
            title = self._extract_title(head)
            published_date = self._extract_published_date(date)
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

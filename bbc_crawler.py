from datetime import datetime

from dateutil.relativedelta import relativedelta
from configobj import ConfigObj

from bbc_article import BBCArticleFetcher


class BBCConfiguration:

    BASE_API_URL = ''
    START_DATE = '2016-01-01'
    END_DATE = '2017-01-01'
    STEP_UNIT = 'day'
    STEP = 1
    PATH = './dataset/bbc/'

    def __init__(self):
        self.base_api_url = self.BASE_API_URL
        self.start_date = datetime.strptime(self.START_DATE, '%Y-%m-%d')
        self.end_date = datetime.strptime(self.END_DATE, '%Y-%m-%d')
        self.step_unit = self.STEP_UNIT
        self.step = relativedelta(days=self.STEP)
        self.path = self.PATH

    def load(self, path):
        config = ConfigObj(path, encoding='UTF-8')
        self.base_api_url = config.get('base_api_url', self.BASE_API_URL)
        self.start_date = datetime.strptime(config.get('start_date', self.START_DATE), '%Y-%m-%d')
        self.end_date = datetime.strptime(config.get('end_date', self.END_DATE), '%Y-%m-%d')
        self.step_unit = config.get('step_unit', self.STEP_UNIT)
        self.step = int(config.get('step', self.STEP))
        if self.step_unit == 'day':
            self.step = relativedelta(days=self.step)
        elif self.step_unit == 'month':
            self.step = relativedelta(months=self.step)
        else:
            self.step = relativedelta(years=self.step)
        self.path = config.get('path', self.PATH)


if __name__ == '__main__':
    config = BBCConfiguration()
    config.load('./settings/bbc.cfg')

    bbc_article_fetcher = BBCArticleFetcher(config)
    bbc_article_fetcher.fetch()

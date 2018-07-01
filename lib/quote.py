from bs4 import BeautifulSoup
import pandas as pd
from lib.util import log
from lib.crawl_base import CrawlBase


class Quote(CrawlBase):
    def __init__(self, code):
        CrawlBase.__init__(self, code)
        self.local= 'data/quote-{}.pickle'.format(self.code)
        self.url = 'https://www.msn.com/en-us/money/stockdetails/fi-137.1.{}.SHE'.format(self.code)

    def parsePage(self, soup):
        data = {}
        ul = soup.find('ul', {'class': 'today-trading-container'})
        liList = ul.findAll('li')
        for li in liList:
            pList = li.findAll('p')
            data[pList[0].getText()] = [pList[1].getText()]
        df = pd.DataFrame(data)
        df.to_pickle(self.local)
        return df
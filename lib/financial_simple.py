from bs4 import BeautifulSoup
import pandas as pd
from lib.util import log
from lib.crawl_base import CrawlBase


class FinancialSimple(CrawlBase):
    def __init__(self, code):
        CrawlBase.__init__(self, code)
        self.local = 'data/fs-{}.pickle'.format(self.code)
        self.url = 'https://www.morningstar.com/stocks/xshe/{}/quote.html'.format(self.code)

    def parsePage(self, soup):
        soupTable = soup.find('table', {'class' : 'report-table ng-isolate-scope'})
        trList = soupTable.findAll('tr')

        ## financial simple
        data = {}
        for tr in trList:
            tds = tr.findAll('td')
            column = [td.getText().strip() for td in tds]
            data[column[0]] = column[1:]

        df = pd.DataFrame(data)
        df.set_index('Fiscal', inplace=True)
        df.to_pickle(self.local)

        return df
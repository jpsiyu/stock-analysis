from lib.util import log
from lib import download_data
import pandas as pd
from lib.statement import Statement

class KeyRatio(Statement):
    def __init__(self, code):
        Statement.__init__(self, code)
        self.df = None
        self.local = 'data/kr-{}.pickle'.format(self.code)

    def download(self):
        url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html'
        queryData = {'t': self.code}
        self.df = download_data.fetchDataIntoPandas(url, queryData, header=2)
        self.reorganizeData()

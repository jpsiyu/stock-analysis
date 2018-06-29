from lib.util import log
from lib import download_data
import pandas as pd
from lib.statement import Statement

class IncomeStatement(Statement):
    def __init__(self, code):
        Statement.__init__(self, code)
        self.df = None
        self.local = 'data/is-{}.pickle'.format(self.code)

    def download(self):
        url, queryData = download_data.createUrlQuery(self.code)
        self.df = download_data.fetchDataIntoPandas(url, queryData)
        self.reorganizeData()

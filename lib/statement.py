import os
import time
from lib.util import log
from lib import download_data
import pandas as pd

class Statement():
    def __init__(self, code):
        self.code = code
        self.df = None
        self.local = 'data/cf-{}.pickle'.format(self.code)

    def fetchData(self, forceDownload=False):
        try:
            diff = time.time() - os.path.getmtime(self.local)
            if forceDownload or diff > 24*3600:
                self.download()
            else:
                self.df = pd.read_pickle(self.local)
                log('Read from local finish')
        except FileNotFoundError as e:
            log("Not found in local")
            self.download()
        except:
            log("Unexpected error:", sys.exc_info()[0])
            raise

    def download(self):
        url, queryData = download_data.createUrlQuery(self.code, reportType='cf', columnYear=10)
        self.df = download_data.fetchDataIntoPandas(url, queryData)
        self.reorganizeData()


    def reorganizeData(self):
        self.df.index.name = None
        if 'TTM' in self.df.columns:
            self.df.drop(labels='TTM', axis='columns', inplace=True)

        self.df = self.df.transpose()
        self.df.index.name = 'Year'
        rowNames = {n: n[0:4] for n in self.df.index}
        self.df.rename(rowNames, axis='index', inplace=True)
        self.df.to_pickle(self.local)
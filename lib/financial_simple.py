from bs4 import BeautifulSoup
import sys
import pandas as pd
from selenium import webdriver
import time
import os
from lib.util import log


class FinancialSimple():
    def __init__(self, code):
        self.code = code
        self.local = 'data/fs-{}.pickle'.format(self.code)
        self.url = 'https://www.morningstar.com/stocks/xshe/{}/quote.html'.format(self.code)
        self.df = None

    def fetchData(self, force=False):
        try:
            diff = time.time() - os.path.getmtime(self.local)
            if force or diff > 24*3600:
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

    def getPage(self):
        try:
            log('Start Crawling Page...')
            option = {
                'executable_path': '/usr/local//Cellar/phantomjs/2.1.1/bin/phantomjs',
                'service_log_path': 'temp/ghostdriver.log',
            }
            driver = webdriver.PhantomJS(**option)
            driver.get(self.url)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.close()
            log('Crawling Page Finish!')
            return soup
        except:
            log('Do not use VPN !!!')
            log('Do not use VPN !!!')
            log('Do not use VPN !!!')
            log('Err:', sys.exc_info()[0])

    def parsePage(self, soup):
        soupTable = soup.find('table', {'class' : 'report-table ng-isolate-scope'})
        trList = soupTable.findAll('tr')

        data = {}
        for tr in trList:
            tds = tr.findAll('td')
            column = [td.getText().strip() for td in tds]
            data[column[0]] = column[1:]

        df = pd.DataFrame(data)
        df.set_index('Fiscal', inplace=True)
        df.to_pickle(self.local)
        return df

    def download(self):
        soup = self.getPage()
        self.df = self.parsePage(soup)
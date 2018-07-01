from bs4 import BeautifulSoup
import sys
import pandas as pd
from selenium import webdriver
import time
import os
from lib.util import log

class CrawlBase():
    def __init__(self, code):
        self.code = code
        self.local = ''
        self.url = ''
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
            log('Sleep...')
            time.sleep(5)
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
        return None

    def download(self):
        soup = self.getPage()
        self.df = self.parsePage(soup)
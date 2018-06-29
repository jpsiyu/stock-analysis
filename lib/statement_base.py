import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as mfm
from sklearn import linear_model
import numpy as np
import re
import os 
from urllib import request

class StatementBase:
    def __init__(self, code):
        self.code = code
        self.df = None
        self.font = self.setFont()
        self.url = 'http://api.xueqiu.com/stock/f10/incstatement.csv?symbol=SZ{}&page=1&size=10000'.format(self.code)
        self.filePath = 'data/incstatement-{}.csv'.format(self.code)


    def setFont(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fontPath= os.path.join(dir_path, '../font/Songti.ttc') 
        font = mfm.FontProperties(fname=fontPath)
        return font

    def downloadData(self):
        opener = request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        request.install_opener(opener)

        request.urlretrieve(self.url, self.filePath)
        print('Good, Down finished!')
        
    def loadData(self):
        self.df = pd.read_csv(self.filePath)
        
    def isAnnual(self, dateInt):
        findList = re.findall('1231$', str(dateInt))
        return len(findList) != 0

    def pickColumns(self, columnList):
        self.df = self.df[columnList]

    def pickAnnual(self, dateColumn, num=10):
        self.df = self.df[self.df[dateColumn].apply(self.isAnnual)].head(num)

    def sort(self, column):
        self.df = self.df.sort_values(by=[column])

    def linearRegresionPredict(self, xdata, ydataInPandas):
        lens = len(xdata)
        fitx = np.array(xdata).reshape(lens, 1)
        fity = ydataInPandas.values.reshape(lens, 1)
        regr = self.modelFit(fitx, fity)
        predy = self.modelPredict(regr, fitx)
        return predy

    def modelFit(self, fitx, fity):
        regr = linear_model.LinearRegression()
        regr.fit(fitx, fity)
        return regr
    
    def modelPredict(self, regr, fitx):
        predy = regr.predict(fitx)
        return predy



    def plot(self, xColName, yColName, title='', xlabel='years', ylabel=''):
        plt.figure(figsize=(12,6))
        xindex = range(self.df.shape[0])
        predy = self.linearRegresionPredict(xindex, self.df[yColName])

        fontSetting = {'fontproperties': self.font, 'size': 18}

        plt.plot(xindex, self.df[yColName])
        plt.plot(xindex, self.df[yColName], 'bo')
        plt.plot(xindex, predy)
        plt.gca().yaxis.grid(True)
        plt.xlabel(xlabel , **fontSetting)
        plt.title(title, **fontSetting)
        plt.ylabel(ylabel, **fontSetting)
        plt.xticks(xindex , self.df[xColName], rotation=70)
        plt.show()

    def customPlot(self, x, y, title='', xlabel='years', ylabel=''):
        fontSetting = {'fontproperties': self.font, 'size': 18}
        plt.figure(figsize=(12,6))
        plt.plot(x, y)
        plt.gca().yaxis.grid(True)
        plt.xlabel(xlabel , **fontSetting)
        plt.title(title, **fontSetting)
        plt.ylabel(ylabel, **fontSetting)
        plt.xticks(x, x, rotation=70)
        plt.show()


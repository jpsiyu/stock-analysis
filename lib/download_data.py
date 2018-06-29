import pandas as pd
from urllib import request
from urllib.parse import urlencode
import io

def createUrlQuery(code, reportType='is', period=12, dataType='A', order='asc', columnYear=10, number=3):
    '''
    code: Tick's symbol
    reportType: is = Income Statement, cf = Cash Flow, bs = Balance Sheet
    period: 12 for annual reporting, 3 for quarterly reporting
    dataType: this doesn't seem to change and is always A
    order: asc or desc (ascending or descending)
    columnYear: 5 or 10 are the only two values supported
    number: The units of the response data. 1 = None 2 = Thousands 3 = Millions 4 = Billions
    api detail: https://gist.github.com/hahnicity/45323026693cdde6a116
    '''

    url = 'http://financials.morningstar.com/ajax/ReportProcess4CSV.html'
    queryData = {
        't': code,
        'reportType': reportType,
        'period': period,
        'dataType': dataType,
        'order': order,
        'columnYear': columnYear,
        'number': number
    } 
    return url, queryData

def fetchDataIntoPandas(url, queryData, header=1):
    opener = request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    request.install_opener(opener)
    
    query = urlencode(queryData).encode('utf-8')

    df = pd.DataFrame()
    with request.urlopen(url, data=query) as response:
        data = response.read()
        df = pd.read_csv(io.StringIO(data.decode('utf-8')), header=2, index_col=0) 
        print('Down finished!')
    return df
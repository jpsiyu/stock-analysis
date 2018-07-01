from lib.income_statement import IncomeStatement
from lib.balance_sheet import BalanceSheet
from lib.cashflow import Cashflow
from lib.key_ratio import KeyRatio
from lib.quote import Quote
from lib.util import log
from lib.dcf import DCF
from lib import plot_tool
import pandas as pd

class Business():
    def __init__(self, code):
        self.code = code
        self.income = IncomeStatement(self.code)
        self.balance = BalanceSheet(self.code)
        self.cashflow = Cashflow(self.code)
        self.keyRatio = KeyRatio(self.code)
        self.quote = Quote(self.code)
        self.dcf = DCF()

    def fetchData(self, force=False):
        self.income.fetchData(force)
        self.balance.fetchData(force)
        self.cashflow.fetchData(force)
        self.keyRatio.fetchData(force)
        self.quote.fetchData(force)
        log('Fetch all data finish!')

    def chartBookValue(self):
        plot_tool.bar(
            self.keyRatio.df.index, 
            self.keyRatio.df['Book Value Per Share * CNY'], 
            title='每股净资产'
        )

    def chartEPS(self):
        plot_tool.bar(
            self.keyRatio.df.index, 
            self.keyRatio.df['Earnings Per Share CNY'],
            title='EPS'
        )

    def chartFCF(self):
        plot_tool.bar(
            self.cashflow.df.index, 
            self.cashflow.df['Free cash flow'],
            title='自由现金流',
        )

    def showDCFReport(self):
        ## dcf calculation
        beta = float(self.quote.df['Beta'].iloc[0])
        taxRate = self.taxRate()
        marketCap = self.marketCap()
        marketDebt = 0
        fcf = self.cashflow.df['Free cash flow']
        factorReport, fcfReport = self.dcf.calculationReport(beta, taxRate, marketCap, marketDebt, fcf, predictYear=5)

        ## valuation
        fcfPresentSum = fcfReport['fcf present'].sum() + fcfReport['terminal value present'].sum()
        value = fcfPresentSum - marketDebt
        shares = self.sharesOutstanding()
        valuePerShare = round(value / shares, 2)
        valueData = {
            'Present Value Sum(M)': [fcfPresentSum],
            'Intrinsic Value(M)': [value],
            'Market Debt(M)': [marketDebt],
            'Shares Outstanding(M)': [shares],
            'Value Per Share': [valuePerShare],
        }
        valuationReport = pd.DataFrame(valueData)
        return factorReport, fcfReport, valuationReport


    def taxRate(self):
        dfTaxRate = self.income.df['Provision for income taxes'] / self.income.df['Income before taxes']
        return round(dfTaxRate.mean(),4)

    def sharesOutstanding(self):
        value = self.quote.df['Shares Outstanding'].iloc[0]
        unit = value[-1]
        if unit == 'B':
            mc = float(value[:-1]) * 1000
        else:
            mc = float(value[:-1])
        return mc


    def marketCap(self):
        value = self.quote.df['Market Cap.'].iloc[0]
        unit = value[-1]
        if unit == 'B':
            mc = float(value[:-1]) * 1000
        else:
            mc = float(value[:-1])
        return mc

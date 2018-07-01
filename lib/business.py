from lib.income_statement import IncomeStatement
from lib.balance_sheet import BalanceSheet
from lib.cashflow import Cashflow
from lib.key_ratio import KeyRatio
from lib.util import log
from lib import plot_tool

class Business():
    def __init__(self, code):
        self.code = code
        self.income = IncomeStatement(self.code)
        self.balance = BalanceSheet(self.code)
        self.cashflow = Cashflow(self.code)
        self.keyRatio = KeyRatio(self.code)

    def fetchData(self, force=False):
        self.income.fetchData(force)
        self.balance.fetchData(force)
        self.cashflow.fetchData(force)
        self.keyRatio.fetchData(force)
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

    def taxRate(self):
        dfTaxRate = self.income.df['Provision for income taxes'] / self.income.df['Income before taxes']
        return round(dfTaxRate.mean(),4)

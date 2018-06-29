import pandas as pd
import numpy as np

class DCF():
    def __init__(self):
        self.riskFree = 3.6
        self.riskPremium = 3.5
        self.perpetuityGrowth = 3

    def costOfEquity(self, beta):
        coe = self.riskFree * 0.01 + self.riskPremium * 0.01 * beta
        return round(coe*100, 2)

    def costOfDebtPreTax(self):
        return 3

    def costOfDebtAfterTax(self, taxRate):
        codPreTax = self.costOfDebtPreTax()
        afterTax = codPreTax * (1 - taxRate * 0.01)
        return round(afterTax, 2)

    def wacc(self, marketValueEquity, equityCost, marketValueDebt, debtCost):
        r = (marketValueEquity * equityCost * 0.01 + marketValueDebt * debtCost * 0.01) / (marketValueEquity + marketValueDebt)
        return round(r*100, 2)

    def calCAGR(self, df):
        start = df.iloc[0]
        end = df.iloc[-1]
        year = df.count()
        cagr = (end/start) ** (1/year) - 1
        return round(cagr*100, 2)

    def predictFCF(self, df, wacc, yearNum=5):
        cagr = self.calCAGR(df)
        mean = df.mean()
        year = df.index.astype(int)[-1]+1
        
        years = np.arange(year, year+yearNum)
        nextYearValue = lambda i: round(mean * ((cagr*0.01 + 1) ** (i+1)), 2)
        predict = [nextYearValue(i) for i, v in enumerate(years)]
        data = {'year': years, 'Free cash flow':predict}
        dfPredict = pd.DataFrame(data)
        dfPredict.set_index('year', inplace=True)

        # discount fcf
        presentValue = lambda i, v: round(v / ((wacc*0.01 + 1) ** (i+1)), 2) 
        discount = [presentValue(i,v) for i, v in enumerate(predict)]
        dfPredict['Discount fcf'] = discount
        return dfPredict

    def terminalValue(self, wacc, fcfEnd, yearNum=5):
        v = fcfEnd * ( 1 + self.perpetuityGrowth * 0.01) / (( wacc - self.perpetuityGrowth) * 0.01)
        vPresent = v / ((1+wacc*0.01) ** yearNum)
        return round(vPresent, 2)





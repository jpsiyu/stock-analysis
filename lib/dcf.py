import pandas as pd
import numpy as np
from sklearn import linear_model

class DCF():
    def __init__(self):
        self.riskFree = 3.6 * 0.01
        self.riskPremium = 3.5 * 0.01
        self.perpetuityGrowth = 3 * 0.01

    def costOfEquity(self, beta):
        coe = self.riskFree + self.riskPremium * beta
        return round(coe, 4)

    def costOfDebtPreTax(self):
        return 0.03

    def costOfDebtAfterTax(self, taxRate):
        codPreTax = self.costOfDebtPreTax()
        afterTax = codPreTax * (1 - taxRate)
        return round(afterTax, 2)

    def wacc(self, marketValueEquity, equityCost, marketValueDebt, debtCost):
        r = (marketValueEquity * equityCost + marketValueDebt * debtCost) / (marketValueEquity + marketValueDebt)
        return round(r, 4)

    def calCAGR(self, df):
        start = df.iloc[0]
        end = df.iloc[-1]
        year = df.count()
        cagr = (end/start) ** (1/year) - 1
        return round(cagr, 4)

    def predictWithCAGR(self, df, yearNum):
        cagr = self.calCAGR(df)
        mean = df.mean()
        year = df.index.astype(int)[-1]+1
        
        years = np.arange(year, year+yearNum)
        nextYearValue = lambda i: round(mean * ((cagr + 1) ** (i+1)), 2)
        predict = [nextYearValue(i) for i, v in enumerate(years)]
        data = {'year': years, 'Free cash flow':predict}
        dfPredict = pd.DataFrame(data)
        dfPredict.set_index('year', inplace=True)
        return dfPredict 

    def predictWithLinearRegression(self, df, yearNum):
        l = df.count()
        fitx = np.array(df.index).reshape(l, 1)
        fity = np.array(df.values).reshape(l, 1)


        module = linear_model.LinearRegression()
        module.fit(fitx, fity)

        year = df.index.astype(int)[-1]+1
        years = np.arange(year, year+yearNum)
        predx = years.reshape(yearNum, 1)
        predy = module.predict(predx)
        
        data = {
            'year': years.ravel(),
            'Free cash flow': predy.ravel(),
        }
        dfPredict = pd.DataFrame(data)
        dfPredict.set_index('year', inplace=True)
        return dfPredict 


    def predictFCF(self, df, wacc, yearNum=5):
        #dfPredict = self.predictWithCAGR(df, yearNum) 
        dfPredict = self.predictWithLinearRegression(df, yearNum) 

        # discount fcf
        presentValue = lambda i, v: round(v / ((wacc + 1) ** (i+1)), 2) 
        discount = [presentValue(i,v) for i, v in enumerate(dfPredict['Free cash flow'])]
        dfPredict['fcf present'] = discount
        return dfPredict

    def terminalValue(self, wacc, fcfEnd, yearNum=5):
        v = fcfEnd * ( 1 + self.perpetuityGrowth ) / (( wacc - self.perpetuityGrowth))
        vPresent = v / ((1+wacc) ** yearNum)
        return (round(v,2), round(vPresent, 2))

        
    def calculationReport(self, beta, taxRate, mvEquity, mvDebt, dfFCF, predictYear=5):
        coe = self.costOfEquity(beta)
        cod = self.costOfDebtAfterTax(taxRate)
        wacc = self.wacc(mvEquity, coe, mvDebt, cod)
        cagr = self.calCAGR(dfFCF)

        factorData = {
            'riskFree': [self.riskFree],
            'riskPremium': [self.riskPremium],
            'perpetuityGrowth': [self.perpetuityGrowth],
            'beta': [beta],
            'costOfEquity': [coe],
            'costOfDebt': [cod],
            'wacc': [wacc],
            'fcfGrowth': [cagr],
            'marketCap': [mvEquity],
            'marketDebt': [mvDebt],
            'taxRate': [taxRate],
        }
        factorReport = pd.DataFrame(factorData)

        predictFCF = self.predictFCF(dfFCF, wacc, yearNum=predictYear)
        endValue, endValuePresent = self.terminalValue(wacc, predictFCF['Free cash flow'].iloc[-1], yearNum=predictYear)

        endValueFuture = [0 for _ in np.arange(predictYear)]
        endValueFuture[-1] = endValue
        predictFCF['terminal value'] = endValueFuture 
        endValueFuture[-1] = endValuePresent
        predictFCF['terminal value present'] = endValueFuture

        return factorReport, predictFCF





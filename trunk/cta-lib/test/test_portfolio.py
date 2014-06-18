'''
Created on 17 juin 2011

@author: julien.bernard
'''
import unittest
from datetime import date, timedelta

from finance.portfolio import Portfolio
from finance.trade import Trade
from finance.cash_flow import CashFlow
from finance.instrument_type import InstrumentType

class MockInstrument(object):
    
    def get_close_value(self, my_date):
        if my_date == date(2000,1,1):
            return 100.
        elif my_date == date(2000,1,2):
            return 105. 
        
    def get_currency(self):
        return 'USD'
    
    def get_type(self):
        return InstrumentType.SINGLE_STOCK
    
    def get_ticker(self):
        return 'MyTicker'

class TestPortfolio(unittest.TestCase):


    def setUp(self):
        self.date = date(2000,1,1)
        
        self.financial_instrument = MockInstrument()


    def testGetValue(self):
        portfolio = Portfolio('USD')
        cash_flow = CashFlow(self.date,1000,'USD') 
        trade = Trade(self.date,self.financial_instrument, 1, self.financial_instrument.get_close_value(self.date))
        cash_flow_trade = CashFlow(self.date, -trade.get_value(self.date, 'USD'),'USD')
        
        portfolio.add_transaction(cash_flow)
        portfolio.add_transaction(trade)
        portfolio.add_transaction(cash_flow_trade)
        
        # check portfolio value at trading date
        self.assertEqual(portfolio.get_value(self.date), 1000, 'initial value')
        
        # check portfolio value after
        other_date = self.date + timedelta(days=1)
        self.assertEqual(portfolio.get_value(other_date), 1005, 'new value')
        
        # check portfolio value before
        other_date = self.date + timedelta(days=-1)
        self.assertEqual(portfolio.get_value(other_date), 0, 'new value')

    def testGetInstrumentQuantity(self):
        portfolio = Portfolio('USD')
        cash_flow = CashFlow(self.date,1000,'USD') 
        trade = Trade(self.date,self.financial_instrument, 10, self.financial_instrument.get_close_value(self.date))
        cash_flow_trade = CashFlow(self.date, -trade.get_value(self.date, 'USD'),'USD')
        
        portfolio.add_transaction(cash_flow)
        portfolio.add_transaction(trade)
        portfolio.add_transaction(cash_flow_trade)
        
        # check the expo
        self.assertEqual(10, portfolio.get_instrument_quantity(self.financial_instrument), 'good quantity')
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAddTransaction']
    unittest.main()
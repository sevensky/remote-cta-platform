'''
@author: julien.bernard
'''
import unittest
from datetime import date

from finance.trade import Trade
from finance.instrument_type import InstrumentType

class MockInstrument(object):
    
    def get_close_value(self, my_date):
        if my_date == date(2000,1,1):
            return 100.
        else:
            return 105. 
        
    def get_currency(self):
        return 'USD'
    
    def get_type(self):
        return InstrumentType.SINGLE_STOCK
    
    def get_ticker(self):
        return 'MyTicker'


class TestTrade(unittest.TestCase):
    
    def setUp(self):
        
        self.date = date(2000,1,1)
    
        self.financial_instrument = MockInstrument()
    
    def testGetValue(self):
        trade = Trade(self.date, self.financial_instrument, 1, self.financial_instrument.get_close_value(self.date))
        
        # check trade is open
        self.assertNotEqual(trade.closed, True, 'trade not closed')
        
        # check get value
        self.assertEqual(trade.get_value(self.date, self.financial_instrument.get_currency()), 100, 'Value day of trade')
        self.assertEqual(trade.get_value(date.today(), self.financial_instrument.get_currency()), 105, 'Value today')

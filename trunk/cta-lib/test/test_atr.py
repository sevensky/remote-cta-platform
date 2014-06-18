import unittest
from finance.math.atr import ATR


class MockInstrument(object):
    
    def get_adjusted_close_value(self, date):
        return 100 + date
    
    def get_high_value(self, date):
        return 110 + date
    
    def get_low_value(self, date):
        return 90 + date

class MockCalendarUtil(object):
    
    def get_n_previous_quote_date(self, instrument, date, n):
        return date - n
    
    def get_next_quote_date(self, instrument, date):
        return date + 1
    
    def get_previous_quote_date(self, instrument, date):
        return date - 1

class TestAtr(unittest.TestCase):


    def testGetValue(self):
        calendar_util = MockCalendarUtil()
        instrument = MockInstrument()
        
        self.assertEqual(ATR.get_value(instrument, 30, 20, calendar_util), 20, 'good ATR')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetValue']
    unittest.main()
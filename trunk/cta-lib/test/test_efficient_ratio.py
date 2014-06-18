import unittest
from finance.math.efficient_ratio import EfficientRatio

class MockInstrument(object):
    
    def get_adjusted_close_value(self, date):
        return 100. + date%2
    
class MockCalendarUtil(object):
    
    def get_n_previous_quote_date(self, instrument, date, n):
        return date - n
    
    def get_next_quote_date(self, instrument, date):
        return date + 1
    
    def get_previous_quote_date(self, instrument, date):
        return date - 1

class TestEfficientRatio(unittest.TestCase):


    def testGetValue(self):
        calendar_util = MockCalendarUtil()
        instrument = MockInstrument()
        
        er = EfficientRatio.get_value(instrument, 15, 5, calendar_util)
        
        self.assertEqual(er, 1./6., 'good efficient ratio')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetValue']
    unittest.main()
'''
Created on 17 juin 2011

@author: julien.bernard
'''
import unittest
from datetime import date, timedelta

from finance.cash_flow import CashFlow

class TestCashFlow(unittest.TestCase):

    def testGetValue(self):
        cash_flow = CashFlow(date.today(),1000,'USD')
        
        # Check get value
        self.assertEqual(cash_flow.get_value(date.today(), 'USD'), 1000, 'value day of cash flow')
        
        tomorow = date.today() + timedelta(days=1)
        self.assertEqual(cash_flow.get_value(tomorow, 'USD'), 1000, 'value day of cash flow')
        
        yesterday = date.today() + timedelta(days=-1)
        self.assertEqual(cash_flow.get_value(yesterday, 'USD'), 0, 'value day of cash flow')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetValue']
    unittest.main()
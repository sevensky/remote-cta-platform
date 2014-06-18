'''
@author: julien.bernard
'''
import unittest
from datetime import date
from finance.calendar_util import CalendarUtil

class MockInstrument(object):
    
    def get_close_value(self, valuation_date):
        
        if valuation_date == date(2011,8,10):
            return 100.0
        elif valuation_date == date(2011,7,29):
            return 50.0

class TestCalendarUtil(unittest.TestCase):


    def testGetNextBusinessDate(self):
        calendar_util = CalendarUtil()
        today = date(2011,6,23)
        tomorow = calendar_util.get_next_business_date(today)
        
        self.assertEqual(tomorow.day, 24, 'push one day')
        
        today = date(2011,6,17)
        tomorow = calendar_util.get_next_business_date(today)
        
        self.assertEqual(tomorow.day, 20, 'push friday to monday')

    def testGetPreviousDate(self):
        calendar_util = CalendarUtil()
        today = date(2011,6,17)
        tomorow = calendar_util.get_previous_business_date(today)
        
        self.assertEqual(tomorow.day, 16, 'push one day')
        
        today = date(2011,6,20)
        tomorow = calendar_util.get_previous_business_date(today)
        
        self.assertEqual(tomorow.day, 17, 'push monday to driday')

    def testGetPreviousQuoteDate(self):
        calendar_util = CalendarUtil()
        today = date(2011,8,10)
        last_date = calendar_util.get_previous_quote_date(today, MockInstrument())
        self.assertEqual(last_date, date(2011,7,29), 'good last quote date')

    def testGetNNextBusinessDate(self):
        calendar_util = CalendarUtil()
        today = date(2011,6,22)
        tomorow = calendar_util.get_n_next_business_date(today, 2)
        
        self.assertEqual(tomorow.day, 24, 'push two days')
        
        today = date(2011,6,17)
        tomorow = calendar_util.get_n_next_business_date(today, 5)
        
        self.assertEqual(tomorow.day, 24, 'push 5 days')

    def testGetNPreviousDate(self):
        calendar_util = CalendarUtil()
        today = date(2011,6,17)
        tomorow = calendar_util.get_n_previous_business_date(today, 2)
        
        self.assertEqual(tomorow.day, 15, 'push two days')
        
        tomorow = calendar_util.get_n_previous_business_date(today, 5)
        
        self.assertEqual(tomorow.day, 10, 'push two days')

    def testIsEndOfWeek(self):
        calendar_util = CalendarUtil()
        day = date(2011,6,17)
        response = calendar_util.is_end_of_week(day)
        
        self.assertEqual(response, True, 'is friday')
        
    def testIsEndOfMonth(self):
        calendar_util = CalendarUtil()
        day = date(2011,6,30)
        response = calendar_util.is_end_of_month(day)
        
        self.assertEqual(response, True, 'is end of month')
        
        day = date(2011,7,29)
        response = calendar_util.is_end_of_month(day)
        
        self.assertEqual(response, True, 'is end of month only business')
        
    def testIsEndOfQuarter(self):
        calendar_util = CalendarUtil()
        day = date(2011,6,30)
        response = calendar_util.is_end_of_quarter(day)
        
        self.assertEqual(response, True, 'is end of quarter')
        
        day = date(2011,7,29)
        response = calendar_util.is_end_of_quarter(day)
        
        self.assertEqual(response, False, 'not end of quarter')
        
    def testIsEndOfYear(self):
        calendar_util = CalendarUtil()
        day = date(2011,6,30)
        response = calendar_util.is_end_of_year(day)
        
        self.assertEqual(response, False, 'is not end of year')
        
        day = date(2011,12,30)
        response = calendar_util.is_end_of_quarter(day)
        
        self.assertEqual(response, True, 'is end of year')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetNextBusinessDate']
    unittest.main()
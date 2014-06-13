'''
Calendar helper
@author: julien.bernard
'''
from datetime import timedelta

class CalendarUtil(object):

    def get_next_business_date(self, date):
        '''
        return the next date, if date is a friday return the next monday
        @param date: the date
        @return the next date 
        '''
        #TODO: manage intraday
        delta = timedelta(days=1)
        next_date = date + delta
        
        if next_date.weekday() in [5,6]:
            next_date = self.get_next_business_date(next_date)
        
        return next_date
        
    def get_previous_business_date(self, date):
        '''
        return the previous date, if date is a monday return the next friday
        @param date: the date
        @return the previous date 
        '''
        #TODO: manage intraday
        delta = timedelta(days=-1)
        previous_date = date + delta
        
        if previous_date.weekday() in [5,6]:
            previous_date = self.get_previous_business_date(previous_date)
        
        return previous_date
    
    def get_previous_quote_date(self, date, instrument):
        '''
        return the previous date for a given instrument
        @param date: the date
        @param instrument: the instrument
        @return: the previous date  
        '''
        #TODO: manage intraday
        iterator_date = self.get_previous_business_date(date)
        while 1:
            value = instrument.get_close_value(iterator_date)
            
            if value:
                return iterator_date
            
            iterator_date = self.get_previous_business_date(iterator_date)
    
    def get_next_quote_date(self, date, instrument):
        '''
        return the next date for a given instrument
        @param date: the date
        @param instrument: the instrument
        @return: the next date  
        '''
        #TODO: manage intraday
        iterator_date = self.get_next_business_date(date)
        while 1:
            value = instrument.get_close_value(iterator_date)
            
            if value:
                return iterator_date
            
            iterator_date = self.get_next_business_date(iterator_date)
    
    def get_n_next_business_date(self, date, n):
        '''
        return the nth next date
        @param date: the date
        @return the next date 
        '''
        i = 1
        result = date
        while i <= n:
            result = self.get_next_business_date(result)
            i=i+1 
            
        return result
    
    def get_n_previous_business_date(self, date, n):
        '''
        return the nth previous date
        @param date: the date
        @return the previous date 
        '''
        i = 1
        result = date
        while i <= n:
            result = self.get_previous_business_date(result)
            i=i+1 
            
        return result

    def get_n_previous_quote_date(self, date, instrument, n):
        '''
        return the nth quote date
        @param date: the date
        @param instrument: the instrument 
        @param n: the number 
        @return: the previous date 
        '''
        i = 1
        result = date
        while i <= n:
            result = self.get_previous_quote_date(result, instrument)
            i=i+1 
            
        return result

    def is_end_of_day(self, date):
        #TODO: manage intraday
        return True

    def is_end_of_week(self, date):
        '''
        return true if date is a Friday
        @param date: the date
        @return true or false
        '''
        return date.weekday() == 4

    def is_end_of_month(self, date):
        '''
        return true if date is business end of month
        @param date: the date
        @return: true or false
        '''
        return date.month <> self.get_next_business_date(date).month
    
    def is_end_of_quarter(self, date):
        '''
        return true if date is business end of quarter
        @param date: the date
        @return: true or false
        '''
        return self.is_end_of_month(date) and date.month%3==0
    
    def is_end_of_year(self, date):
        '''
        return true if date is business end of year
        @param date: the date
        @return: true or false
        '''
        return date.year <> self.get_next_business_date(date).year
        
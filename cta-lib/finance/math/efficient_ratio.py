'''
Kaufman efficient ratio (strength of trend)
@author: julien.bernard
'''

class EfficientRatio(object):
    
    @staticmethod
    def get_value(instrument, date, depth, calendar_util):
        '''
        return the efficient ratio n value for a given instrument
        @param instrument: the instrument
        @param date: the date
        @param depth: the depth
        @param calendar_util: the calendar util     
        '''
        minus_n_date = calendar_util.get_n_previous_quote_date(instrument=instrument,
                                                               date=date, n=depth)
        
        numerator = abs(instrument.get_adjusted_close_value(date) - 
                        instrument.get_adjusted_close_value(minus_n_date))
        
        denominator = 0
        
        current_date = date
        
        while current_date >= minus_n_date:
            last_date = calendar_util.get_previous_quote_date(instrument=instrument,
                                                                 date=current_date)
            
            denominator += abs(instrument.get_adjusted_close_value(current_date)-
                               instrument.get_adjusted_close_value(last_date))
            
            current_date = last_date
            
        return numerator/denominator

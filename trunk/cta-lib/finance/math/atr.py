'''
Average true range on continuous contract
@author: julien.bernard
'''

import numpy

class ATR(object):
    
    @staticmethod
    def _get_true_range(instrument, date, calendar_util):
        high_low = instrument.get_high_value(date) - instrument.get_low_value(date)
        last_date = calendar_util.get_previous_quote_date(instrument=instrument, date=date)
        close_high = instrument.get_high_value(date) - instrument.get_adjusted_close_value(last_date) 
        close_low = instrument.get_adjusted_close_value(last_date) - instrument.get_low_value(date)
        
        return numpy.amax([high_low,close_high,close_low])
    
    @staticmethod
    def get_value(instrument, date, depth, calendar_util):
        '''
        get an ATR value at a given date
        @param instrument: the instrument
        @param depth: the depth 
        @param date: the computation date
        @param calendar_util: the calendar util
        @return: the ATR value
        '''
        
        iterator_date = calendar_util.get_n_previous_quote_date(instrument=instrument,
                                                               date=date, n=depth)
        true_range = []
        while iterator_date <= date:
            current_true_range = ATR._get_true_range(instrument, iterator_date, calendar_util)
            true_range.append(current_true_range)
            iterator_date = calendar_util.get_next_quote_date(instrument=instrument,
                                                              date=iterator_date)
            
        return float(numpy.mean(true_range))        
        
            
        
        
        
        
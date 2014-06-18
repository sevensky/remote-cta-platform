'''
Risk units quantity computer
@author: julien.bernard
'''
from finance.math.atr import ATR

class UnitsComputer(object):
    
    def __init__(self, id, strategy):
        
        self.id = id
        
        self.strategy = strategy
        
    def get_quantity_to_trade(self, instrument, value, date):
        '''
        return the number of instrument to trade to exposed to the asked nb units
        @param instrument: the instrument
        @param value: the number units
        @param date: the date
        @return: the quantity of instruments   
        '''
        
        calendar_util = self.strategy.calendar_util
        ptf_value = self.strategy.portfolio.get_value(date)
        current_atr = ATR.get_value(instrument, date, 21, calendar_util)
        
        return value*0.001*ptf_value/current_atr
        
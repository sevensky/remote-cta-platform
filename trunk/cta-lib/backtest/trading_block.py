'''
A strategy component, contains the conditions, the allocation.
@author: julien.bernard
'''
from core_error import CoreError
from finance.order_type import OrderType

class TradingBlock(object):
    
    
    def __init__(self, id):
        
        self.id = id
        
        # list of condition bundles
        self.conditions = []
    
        self.order_type = None
    
        self.raw_quantity = None
    
        self.quantity_computer = None
    
        self.instrument = None
        
        self.calendar_util = None
        
    def is_active(self, date):
        '''
        return true if all conditions is active at a date
        @param date: the date 
        @return:true or false
        '''
        is_active = True
        
        for cond in self.conditions:
            is_active = is_active and cond.is_active(date)
            
        return is_active
    
    def get_quantity_to_trade(self, date):
        '''
        return quantity of instrument to trade
        @param date: the trading date
        @raise CoreError:  
        '''
        
        qty = self.quantity_computer.get_quantity_to_trade(instrument=self.instrument, 
                                                           value=self.raw_quantity, 
                                                           date=date)
            
        if qty < 0:
            raise CoreError('quantity computer return a negative quantity')
            
        if self.order_type == OrderType.SELL:
            qty = qty*-1
            
        return qty
            
    def __repr__(self):
        return self.id
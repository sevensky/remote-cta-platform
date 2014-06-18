'''
Trade class, transaction on instrument
@author: julien.bernard
'''
from finance.instrument_type import InstrumentType
from finance.cash_flow import CashFlow

class Trade(object):
    
    def __init__(self, date, instrument, quantity, price):
        self.date = date
        self.price = price
        self.instrument = instrument
        self.quantity = quantity
        self.closed = False
        self.last_value = None
        
    def get_value(self, date, currency):
        '''
        get the value of trade, if trade is closed return 0
        @param date: the valuation date 
        '''
        if self.closed:
            return 0.0
        
        if date < self.date:
            return 0.
        
        if self.instrument.get_currency() == currency:
            value = self.instrument.get_close_value(date)
            
            if value:
                # check instrument type to compute value
                if self.instrument.get_type() == InstrumentType.FUTURE:
                    self.last_value = (value - self.price) * self.quantity
                else:
                    self.last_value = value * self.quantity
            
            return self.last_value
        
        raise NotImplementedError('Exchange rate value')
    
    def close(self, exit_date, exit_price):
        '''
        compute and return the cash flow related to realized p&l and close the trade
        @param exit_date: the exit date 
        @param exit price: the exit price 
        '''
        cash_flow = 0.
        if self.closed == False:
            cash_flow = self.quantity*(exit_price - self.price)
        
        self.closed = True
        
        return CashFlow(exit_date, cash_flow, self.instrument.get_currency())
    
    def __repr__(self):
        qty_to_display = self.quantity / self.instrument.get_point_value()
        return '%s: %i %s @ %f'%(self.date, qty_to_display, self.instrument, self.price)    
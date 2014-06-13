'''
Compute the quantity related to the nominal asked
@author: julien.bernard
'''
class NominalComputer(object):
    
    def __init__(self, id, strategy):
        self.id = id
        
        self.strategy = strategy
    
    def get_quantity_to_trade(self, instrument, value, date):
        '''
        return the number of instrument to trade to exposed to the asked value
        @param instrument: the instrument
        @param value: the nominal
        @param date: the date
        @return: the quantity of instruments   
        '''
        ptf_value = self.strategy.portfolio.get_value(date)
        instrument_value = instrument.get_close_value(date)
        qty = 0.
        
        if instrument.get_currency() == self.strategy.portfolio.currency:
            qty = value*ptf_value/instrument_value
        else:
            raise NotImplementedError('Not yet implemented for multi currency')
        
        return qty

'''
@author: julien.bernard
'''
from finance.financial_instrument import FinancialInstrument

class FutureContract(FinancialInstrument):
    
    def __init__(self, instrument, entry_price):
        FinancialInstrument.__init__(self, instrument)
        self.entry_price = entry_price
        
    def get_adjusted_close_value(self, date):
        return FinancialInstrument.get_adjusted_close_value(self, date) - self.entry_price
    
    def get_close_value(self, date):
        return FinancialInstrument.get_close_value(self, date) - self.entry_price
    
    def get_open_value(self, date):
        return FinancialInstrument.get_open_value(self, date) - self.entry_price
    
    def get_high_value(self, date):
        return FinancialInstrument.get_high_value(self, date) - self.entry_price
    
    def get_low_value(self, date):
        return FinancialInstrument.get_low_value(self, date) - self.entry_price
    
    def is_need_cash(self):
        return False
'''
Portfolio instrument container which has a value
@author: julien.bernard
'''
from finance.trade import Trade

class Portfolio(object):
    
    
    def __init__(self, currency):
        self.transactions = []
        self.currency = currency
        
    def add_transaction(self, transaction):
        '''
        Add a transaction to portfolio
        @param transation: the transaction 
        '''
        self.transactions.append(transaction)
        
    def get_value(self, date):
        '''
        Get the value of portfolio at a date
        @param date: the date
        @return: the portfolio value 
        '''
        
        value = 0.0
        
        # value of transactions
        for trans in self.transactions:
            value += trans.get_value(date, self.currency)
        
        if value < 0:
            return 0
        
        return value
    
    def get_instrument_quantity(self, instrument):
        '''
        return the quantity of instrument in the portfolio
        @param instrument: the instrument 
        '''
        qty = 0
        for trade in self.transactions:
            if isinstance(trade, Trade) and not trade.closed:
                if trade.instrument.get_ticker() == instrument.get_ticker():
                    qty += trade.quantity
        
        return qty
    

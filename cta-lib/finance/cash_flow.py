'''
@author: julien.bernard
'''

class CashFlow(object):
    
    def __init__(self, date, amount, currency):
        self.date = date
        self.amount = amount
        self.currency = currency
        
    def get_value(self, date, currency):
        '''
        Compute the cash flow value
        @param date: the valuation date
        @return: the value 
        '''
        
        if self.currency == currency:
            if date < self.date:
                return 0
            else:
                return self.amount
        
        raise NotImplementedError('Exchange rate value')
        
    def __repr__(self):
        return '%s: %f %s'%(self.date, self.amount, self.currency)
        
    

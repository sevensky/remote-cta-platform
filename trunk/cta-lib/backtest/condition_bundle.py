'''
Class which contains a regime and an indicator
@author: julien.bernard
'''

class ConditionBundle(object):
    
    
    def __init__(self, regime=None, indicator=None):
        self.regime = regime
    
        self.indicator = indicator
        
    def is_active(self, date):
        '''
        return true if condition is true at a date
        @param date: the date
        @return: true or false
        '''
        current_regime = self.indicator.get_regime(date)
        
        return current_regime == self.regime
        

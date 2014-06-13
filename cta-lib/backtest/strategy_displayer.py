'''
Utils class to display strategy results

@author: julien.bernard
'''
from finance.math.financial_statistics import FinancialStatistics

class StrategyDisplayer(object):
    
    def __init__(self, strategy):
        
        self.strategy = strategy
        
    def display_statistics(self):
        '''
        display strategy all implemented strategy statistics
        '''
        
        stats = FinancialStatistics.get_statistics(self.strategy)
        name = self.strategy.name
        for stat_name, stat_value in stats.items():
            print '%s\t%s\t%f'%(name, stat_name, stat_value)

    def display_equity_curve(self):
        '''
        display daily equity curve
        '''
        calendar_util = self.strategy.calendar_util
        
        iterator = self.strategy.first_date
        
        print 'Strat\tDate\tValue'
        while iterator <= self.strategy.last_date:
            print '%s\t%s\t%f'%(self.strategy.name, iterator,self.strategy.track_record[iterator])
            iterator = calendar_util.get_next_business_date(iterator)
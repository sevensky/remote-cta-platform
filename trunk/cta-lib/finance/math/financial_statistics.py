'''
Compute all type of financial statistics
@author: julien.bernard
'''

import numpy
from scipy import stats

class FinancialStatistics(object):
    
    ANNUALIZED_COMPOUND = 'Annualized Compound'
    
    ANNUALIZED_VOLATILITY = 'Annualized Volatility'
    
    SHARPE_RATIO = 'Sharpe Ratio'
    
    MIN_RETURN = 'Minimun Return'
    
    MAX_RETURN = 'Maximum Return'
    
    SKEWNESS = 'Skewness'
    
    KURTOSIS = 'Kurtosis'
    
    @staticmethod
    def get_statistics(strategy):
        '''
        Return a dict of statistics
        @param strategy: the strategy 
        '''
        
        statistics = {}
        # compute returns
        returns = FinancialStatistics._get_strategy_returns(strategy)
        cash_returns = FinancialStatistics._get_cash_returns(strategy)
        
        
        # compute mean returns
        mean = FinancialStatistics._get_mean(returns)
        cash_mean = FinancialStatistics._get_mean(cash_returns)
        
        # compute returns variance
        variance = FinancialStatistics._get_variance(returns)
        
        # compute annualized compound
        compound = FinancialStatistics._get_annualized_compound(returns)
        
        # compute annualized volatility
        statistics[FinancialStatistics.ANNUALIZED_VOLATILITY] = 252**(.5)*variance**(.5)
        
        # compute sharpe ratio
        statistics[FinancialStatistics.SHARPE_RATIO] = 252**(.5)*(mean - cash_mean)/(variance**(.5))
        
        # compute the minimum and maximum return
        statistics[FinancialStatistics.MIN_RETURN] = numpy.min(returns)
        statistics[FinancialStatistics.MAX_RETURN] = numpy.max(returns)
        
        # compute skewness and kurtosis
        statistics[FinancialStatistics.SKEWNESS] = stats.skew(returns)
        statistics[FinancialStatistics.KURTOSIS] = stats.kurtosis(returns)
        
        statistics[FinancialStatistics.ANNUALIZED_COMPOUND] = compound
        
        return statistics
        
    @staticmethod
    def _get_strategy_returns(strategy):
        
        returns = []
        last_value = None
        compute_date = strategy.first_date
        
        while compute_date <= strategy.last_date:
            value = strategy.track_record[compute_date]
            
            if last_value:
                returns.append(value/last_value-1)
        
            last_value = value
            compute_date = strategy.calendar_util.get_next_business_date(compute_date)
        
        return returns
    
    @staticmethod
    def _get_cash_returns(strategy):
        returns = []
        compute_date = strategy.first_date
        
        while compute_date <= strategy.last_date:
            if strategy.portfolio.currency in strategy.interest_rates:
                rate_value = strategy.interest_rates[strategy.portfolio.currency].get_close_value(compute_date)
                t = compute_date - strategy.calendar_util.get_previous_business_date(compute_date)
                rate_daily = (1.+rate_value)**(t.days/365.)-1
                returns.append(rate_daily)
            else:
                returns.append(0.)
            
            compute_date = strategy.calendar_util.get_next_business_date(compute_date)
        
        return returns
    
    @staticmethod
    def _get_mean(returns):
        return numpy.mean(returns)
    
    @staticmethod
    def _get_variance(returns):
        return numpy.var(returns)
    
    @staticmethod
    def _get_annualized_compound(returns):
        product = 1.
        
        for value in returns:
            product = product*(1+value)
            
        return product**(252./float(len(returns))) - 1

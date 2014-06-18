'''
Listener which listen to valorization event to compute portfolio position and compute cash reward
@author: julien.bernard
'''
from backtest.listener.abstract_listener import AbstractListener
from finance.cash_flow import CashFlow
from core_error import CoreError
import logging
from finance.trade import Trade

class ValorizationListener(AbstractListener):
    
    logger = logging.getLogger('ValorizationListener')
    
    def process_event(self, event):
        '''
        get an event (valorization event) and compute the end of trading day
        @param event: the valorization event 
        @raise CoreError:  
        '''
        
        portfolio = self.strategy.portfolio
        date = event.datas['date']
        
        # erase trade closed, aggregate cash flow and erase them
        transactions_to_erase = []
        currency_positions = {}
        for trans in portfolio.transactions:
            if isinstance(trans, Trade):
                if trans.closed:
                    transactions_to_erase.append(trans)
            if isinstance(trans, CashFlow):
                if trans.currency in currency_positions:
                    currency_positions[trans.currency] += trans.amount 
                else:
                    currency_positions[trans.currency] = trans.amount
                transactions_to_erase.append(trans)
                
                    
        for trade in transactions_to_erase:
            portfolio.transactions.remove(trade)
        
        # compute the capitalization cash flow
        yesterday = self.strategy.calendar_util.get_previous_business_date(date)
        t = date - yesterday
        
        for currency, amount in currency_positions.items():
            # build new cash flow and put it in portfolio
            global_cash_flow = CashFlow(date, amount, currency)
            portfolio.add_transaction(global_cash_flow)
            
            # build capitalization cash flow
            if currency in self.strategy.interest_rates:
                rate_value = self.strategy.interest_rates[currency].get_close_value(date)
                rate_daily = (1.+rate_value)**(t.days/365.)-1
                
                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug('%s: capitalization %d %s @ %d'%(date,amount*rate_daily,currency,rate_value*100) + '%')
                
                cash_flow = CashFlow(date, amount*rate_daily, currency)
                portfolio.add_transaction(cash_flow)
            else:
                if len(self.strategy.interest_rates) != 0:
                    raise CoreError('No interest rate for %s'%currency)
                
        # freeze portfolio value in strategy'strack record
        self.strategy.track_record[date] = portfolio.get_value(date)
        
        if self.logger.isEnabledFor(logging.INFO):
            self.logger.info('portfolio value %s: %f'%(date, self.strategy.track_record[date]))
        
        if self.logger.isEnabledFor(logging.INFO):
            for transaction in portfolio.transactions:
                self.logger.info('TRANSACTION --> %s'%transaction)
        
        

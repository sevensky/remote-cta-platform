'''
Listener dedicated to portfolio update
@author: julien.bernard
'''
from finance.trade import Trade
from finance.cash_flow import CashFlow
from backtest.listener.abstract_listener import AbstractListener
import logging

class TradingListener(AbstractListener):
    
    logger = logging.getLogger('TradingListener')
    
    def process_event(self, event):
        '''
        Build the trade, the related cash flow and put it in portfolio
        @param event: the trading event
        '''
        
        qty = event.datas['quantity']
        instrument = event.datas['instrument']
        date = event.datas['date']
        price = event.datas['price']
        closing = event.datas['closing']
        
        fees = 0.
        if instrument.get_transactions_fees():
            fees = instrument.get_transactions_fees()
            
        currency = instrument.get_currency()
        portfolio = self.strategy.portfolio
        
        # check if it is an opening trade
        if not closing:
            
            #  compute trading price
            if qty > 0:
                price += fees
            else:
                price -= fees
            
            # build trade
            trade = Trade(date, instrument, qty, price)
        
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug('add trade: %s'%trade)
        
            portfolio.add_transaction(trade)
        
            if instrument.is_need_cash():
                
                cash_flow = CashFlow(date, -qty*price, currency)
                
                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug('add cash flow: %s'%cash_flow)
                
                portfolio.add_transaction(cash_flow)
                
        # else it is a closing trade
        else:
            for trans in portfolio.transactions:
                if isinstance(trans, Trade):
                    if trans.instrument.get_ticker() == instrument.get_ticker():
                        qty = trans.quantity
                        
                        if qty > 0:
                            price += fees
                        else:
                            price -= fees
                        
                        pnl = trans.close(date, price)
                        
                        if self.logger.isEnabledFor(logging.DEBUG):
                            self.logger.debug('close trade: %s'%trans)
                            self.logger.debug('add cash flow: %s'%pnl)
                        
                        portfolio.add_transaction(pnl)

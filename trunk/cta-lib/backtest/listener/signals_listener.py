'''
Listener which listen to signals event
@author: julien.bernard
'''
from backtest.listener.abstract_listener import AbstractListener
from backtest.event import Event

class SignalsListener(AbstractListener):
    
    def process_event(self, event):
        '''
        get an event (signal event) which contains changing trading blocks and send trade event
        @param event: the event (signal event)
        @raise CoreError:  
        '''
        instrument = event.datas['instrument']
        date = event.datas['date']
        
        # map instruments and quantities
        trades = {}
        
        # fill the map
        for block in self.strategy.trading_blocks[instrument]:
            qty = 0.0
            # if block is active trade a new signal else close an old signal
            if block.is_active(date):
                # compute target quantity
                qty = block.get_quantity_to_trade(date)
                
            if instrument in trades:
                trades[instrument] = trades[instrument] + qty
            else:
                trades[instrument] = qty
        
        # compute real quantity to trade and send event    
        for instrument in trades:
            qty_to_trade =  trades[instrument] - self.strategy.portfolio.get_instrument_quantity(instrument)
            # if trade already performed in the rolling
            if qty_to_trade != 0:
                trade_event = Event(Event.TRADE_EVENT)
                trade_event.datas['date'] = date
                trade_event.datas['instrument'] = instrument
                trade_event.datas['closing'] = False
                trade_event.datas['quantity'] = qty_to_trade
                trade_event.datas['price'] = instrument.get_close_value(date)
                self.strategy.event_dispatcher.dispatch_event(trade_event) 
            
        
        
        
        
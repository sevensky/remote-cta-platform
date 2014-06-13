'''
Listen rolling event and send a trading event.
@author: julien.bernard
'''
from backtest.listener.abstract_listener import AbstractListener
from backtest.event import Event

class RollingListener(AbstractListener):
    
    def _get_close_trade_price(self, instrument, date):
        
        # check if it is a maturity rolling or a simple rolling
        if instrument.get_reference_month(date):
            back_date = self.strategy.calendar_util.get_previous_quote_date(date, instrument)
            
            # if it is a future maturity rolling then return the previous contract value
            if instrument.get_reference_month(date) != instrument.get_reference_month(back_date):
                price = instrument.get_close_value(back_date) + (instrument.get_adjusted_close_value(date) 
                                                                 - instrument.get_adjusted_close_value(back_date))
                return price
            
        # else return the current contract value
        return instrument.get_close_value(date)
            
    
    def process_event(self, event):
        '''
        get a rolling event, build the trade event
        @param event: the rolling event
        '''
        date = event.datas['date']
        instrument = event.datas['instrument']
        
        # select block to roll and map raw quantity with related instrument
        quantity = 0.
        for block in self.strategy.trading_blocks[instrument]:
            if block.is_active(date):
                quantity += block.get_quantity_to_trade(date)
        
        event_dispatcher = self.strategy.event_dispatcher
        
        
        close_trade_event = Event(Event.TRADE_EVENT)
        close_trade_event.datas['date'] = date
        close_trade_event.datas['quantity'] = 0.
        close_trade_event.datas['instrument'] = instrument
        close_trade_event.datas['price'] = self._get_close_trade_price(instrument, date)
        close_trade_event.datas['closing'] = True
        event_dispatcher.dispatch_event(close_trade_event)
            
        # the new trade event
        new_trade_event = Event(Event.TRADE_EVENT)
        new_trade_event.datas['date'] = date
        new_trade_event.datas['quantity'] = quantity
        new_trade_event.datas['instrument'] = instrument
        new_trade_event.datas['price'] = instrument.get_close_value(date)
        new_trade_event.datas['closing'] = False
        event_dispatcher.dispatch_event(new_trade_event)
            
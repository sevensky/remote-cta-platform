'''
Listener for trade time event, if receive an event then sent an event to compute signals or rolling
@author: julien.bernard
'''
from backtest.event import Event
from backtest.rolling import Rolling
from core_error import CoreError
from backtest.listener.abstract_listener import AbstractListener
import logging

class TradingTimeListener(AbstractListener):
    
    logger = logging.getLogger('TradingTimeListener')
    
    def _is_rolling(self, event):
        
        date = event.datas['date']
        
        # if date equals to strategy first date return false
        if date == self.strategy.first_date or date == self.strategy.last_date:
            return False
        
        # switch case to detect if date is end of period
        if self.strategy.rolling == Rolling.END_OF_DAY:
            return self.strategy.calendar_util.is_end_of_day(date)
        elif self.strategy.rolling == Rolling.END_OF_WEEK:
            return self.strategy.calendar_util.is_end_of_week(date)
        elif self.strategy.rolling == Rolling.END_OF_MONTH:
            return self.strategy.calendar_util.is_end_of_month(date)
        elif self.strategy.rolling == Rolling.END_OF_QUARTER:
            return self.strategy.calendar_util.is_end_of_quarter(date)
        elif self.strategy.rolling == Rolling.END_OF_YEAR:
            return self.strategy.calendar_util.is_end_of_year(date)
        else:
            raise CoreError('No rolling %s'%self.strategy.rolling)
        
        return False
        
    def process_event(self, event):
        '''
        get an event (trading time event), check if date is a rolling day and command
        computation of signals
        @param event: trading time event 
        '''
        event_dispatcher = self.strategy.event_dispatcher
        date = event.datas['date']
        instrument = event.datas['instrument']
        
        # check if it is a portfolio rolling time
        if self._is_rolling(event):
            rolling_event = Event(Event.ROLLING_EVENT)
            # transfer the date from trading time event to rolling event
            rolling_event.datas['date'] = date 
            rolling_event.datas['instrument'] = instrument
            event_dispatcher.dispatch_event(rolling_event)
        else:
            # check if there are some contract to roll
            if instrument.get_reference_month(date):
                back_date = self.strategy.calendar_util.get_previous_quote_date(date, instrument)
                if instrument.get_reference_month(date) != instrument.get_reference_month(back_date):
                    future_rolling_event = Event(Event.ROLLING_EVENT)
                    future_rolling_event.datas['date'] = date
                    future_rolling_event.datas['instrument'] = instrument
            
                    event_dispatcher.dispatch_event(future_rolling_event)
        
        # check condition and send signal event
        signals_active = False
        for block in self.strategy.trading_blocks[instrument]:
            
            is_block_active = block.is_active(date)
            
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug('%s %i'%(block,is_block_active))
            
            # if signal configuration change store the block
            if is_block_active != self.strategy.trading_blocks_state[block]:
                signals_active = True
                # update strategy trading block
                self.strategy.trading_blocks_state[block] = block.is_active(date)
        
        # send event with changing blocks        
        if signals_active:
            signal_event = Event(Event.SIGNALS_EVENT)
            signal_event.datas['instrument'] = instrument
            signal_event.datas['date'] = date
            event_dispatcher.dispatch_event(signal_event)
        
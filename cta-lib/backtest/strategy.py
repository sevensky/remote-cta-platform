'''
Event machine to launch a strategy
@author: julien.bernard
'''

from backtest.dispatcher import EventDispatcher
from finance.calendar_util import CalendarUtil
from backtest.event import Event
from backtest.listener.time_listener import TradingTimeListener
from backtest.listener.rolling_listener import RollingListener
from backtest.listener.trading_listener import TradingListener
from backtest.condition_bundle import ConditionBundle
from backtest.listener.signals_listener import SignalsListener
import logging
from core_error import CoreError
from backtest.listener.valorization_listener import ValorizationListener

class Strategy(object):
    
    logger = logging.getLogger('Strategy')
    
    def __init__(self, name):
        
        self.name = name
        
        # strategy data
        self.first_date = None
    
        self.last_date = None
    
        self.portfolio = None
    
        # map ticker and instrument 
        self.instruments = {}
    
        # map ID and indicator
        self.indicators = {}
    
        # map ID and quantity computer
        self.quantity_computers = {}
    
        # map instrument and list of trading blocks
        self.trading_blocks = {}
    
        # map blocks and last state
        self.trading_blocks_state = {}
    
        # map currency and financial instrument (interest rate)
        self.interest_rates = {}
    
        self.rolling = None
        
        # track record map date and portfolio value
        self.track_record = {}
        
        # other objects
        self.event_dispatcher = EventDispatcher()
    
        self.calendar_util = CalendarUtil()
        
        # setup the event dispatcher
        self.event_dispatcher.add_event_listener(Event.TRADING_TIME_EVENT, TradingTimeListener(self))
        self.event_dispatcher.add_event_listener(Event.ROLLING_EVENT, RollingListener(self))
        self.event_dispatcher.add_event_listener(Event.TRADE_EVENT, TradingListener(self))
        self.event_dispatcher.add_event_listener(Event.SIGNALS_EVENT, SignalsListener(self))
        self.event_dispatcher.add_event_listener(Event.VALORIZATION_EVENT, ValorizationListener(self))
    
    def add_instrument(self, instrument):
        '''
        Add instrument to stategy instrument map
        @param instrument: the financial instrument 
        '''
        if instrument.get_ticker() not in self.instruments:
            self.instruments[instrument.get_ticker()] = instrument
            
    def add_indicator(self, indicator):
        '''
        Add indicator to strategy indicator map
        @param indicator: the indicator 
        '''
        if indicator.id not in self.indicators:
            self.indicators[indicator.id] = indicator
    
    def add_quantity_computer(self, quantity_computer):
        '''
        Add a quantity computer to strategy quantity computer map
        @param quantity_computer: the quantity computer 
        '''
        if quantity_computer.id not in self.quantity_computers:
            self.quantity_computers[quantity_computer.id] = quantity_computer
        
    def add_trading_block(self, trading_block):
        '''
        Add trading block to strategy trading block map and by default set last state to false
        @param trading_block: the trading block 
        '''
        
        # add calendar util to trading block
        trading_block.calendar_util = self.calendar_util
        
        # map instrument's block and block
        if trading_block.instrument in self.trading_blocks:
            self.trading_blocks[trading_block.instrument].append(trading_block)
        else:
            self.trading_blocks[trading_block.instrument] = [trading_block]
         
        if trading_block not in self.trading_blocks_state:
            self.trading_blocks_state[trading_block] = False
    
    def add_condition_bundle_to_trading_block(self, trading_block, regime, indicator):
        '''
        Add a condition bundle to a trading block
        @param trading_block_id: the trading block 
        @param regime: the regime
        @param indicator_id: the indicator   
        '''
        if trading_block in self.trading_blocks_state:
            if indicator.id in self.indicators:
                condition_bundle = ConditionBundle()
                condition_bundle.regime = regime
                condition_bundle.indicator = indicator
                trading_block.conditions.append(condition_bundle)
        
    
    def add_quantity_computer_to_trading_block(self, trading_block, computer, raw_quantity):
        '''
        Add a quantity computer to a trading block
        @param trading_block_id: the trading block
        @param computer_id: the computer
        @param raw_quantity: the raw quantity  
        '''
        if trading_block in self.trading_blocks_state:
            if computer.id in self.quantity_computers:
                trading_block.quantity_computer = computer
                trading_block.raw_quantity = raw_quantity
            
    
    def add_interest_rate(self, currency, financial_instrument):
        '''
        Add an interest rate to strategy for a given currency
        @param currency: the currency
        @param financial_instrument: the financial_instrument
        @raise CoreError: if financial instrument quotes in a different currency   
        '''
        if currency == financial_instrument.get_currency():
            self.interest_rates[currency] = financial_instrument
        else:
            raise CoreError('financial instrument currency quotes in %s for currency %s'%(financial_instrument.get_currency(),currency))
          
    def compute(self):
        '''
        compute the strategy
        @raise CoreError: 
        '''
           
        compute_date = self.first_date
        
        while compute_date <= self.last_date:
            
            # check if it is instrument trading day
            for instrument in self.instruments.values():
                value = instrument.get_close_value(compute_date)
                
                # if there is a value then send trading time event
                if value:
                    trading_time_event = Event(Event.TRADING_TIME_EVENT)
                    trading_time_event.datas['date'] = compute_date
                    trading_time_event.datas['instrument'] = instrument
                    
                    if self.logger.isEnabledFor(logging.DEBUG):
                        self.logger.debug('%s: send event %s'%(compute_date,trading_time_event.type))
                    
                    self.event_dispatcher.dispatch_event(trading_time_event)
            
                
            
            # build valorization event and send it
            valo_event = Event(Event.VALORIZATION_EVENT)
            valo_event.datas['date'] = compute_date
            
            self.event_dispatcher.dispatch_event(valo_event)
            
            compute_date = self.calendar_util.get_next_business_date(compute_date)
            
    def __str__(self):
        return self.name
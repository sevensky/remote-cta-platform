'''
Service which computes and returns backtest
'''
from backtest.computer.computer_type import ComputerType
from backtest.computer.nominal_computer import NominalComputer
from backtest.computer.units_computer import UnitsComputer
from backtest.indicator.digital_filter_indicator import DigitalFilterIndicator
from backtest.indicator.ema import Ema
from backtest.indicator.frama import Frama
from backtest.indicator.indicator_type import IndicatorType
from backtest.indicator.kama import Kama
from backtest.indicator.sma import Sma
from backtest.indicator.vidya import Vidya
from backtest.strategy import Strategy
from backtest.trading_block import TradingBlock
from datetime import datetime
from finance.cash_flow import CashFlow
from finance.financial_instrument import FinancialInstrument
from finance.portfolio import Portfolio
from instrument_service import InstrumentService
from server_error import ServerError

class BacktestService(object):
    
    def __init__(self):
        
        self.instrument_service = InstrumentService()
    
    def get_indicator(self, indicator_settings, backtest_settings, instrument):
        '''
        return an indicator with its parameters, building type and instrument from indicator settings
        @param indicator_settings: the indicator_settings
        @return: the indicator
        @raise ServiceError:     
        '''
        
        # build the indicator
        indicator_type = indicator_settings['indicator_type']
        building_type = indicator_settings['building_type']
        parameters = map(float, indicator_settings['parameters'].split('_'))
        indicator_id = indicator_settings['name']
        
        if indicator_type in (IndicatorType.BESSEL, IndicatorType.BUTTERWORTH, IndicatorType.CHEBYSCHEV):
            indicator = DigitalFilterIndicator(indicator_id, indicator_type, building_type, instrument, parameters)
        elif indicator_type == IndicatorType.KAMA:
            indicator = Kama(indicator_id, indicator_type, building_type, instrument, parameters)
        elif indicator_type == IndicatorType.VIDYA:
            indicator = Vidya(indicator_id, indicator_type, building_type, instrument, parameters)
        elif indicator_type == IndicatorType.EMA:
            indicator = Ema(indicator_id, indicator_type, building_type, instrument, parameters)
        elif indicator_type == IndicatorType.SMA:
            indicator = Sma(indicator_id, indicator_type, building_type, instrument, parameters)
        elif indicator_type == IndicatorType.FRAMA:
            indicator = Frama(indicator_id, indicator_type, building_type, instrument, parameters)

        return indicator
        
    def get_quantity_computer(self, quantity_computer_type, strategy):
        '''
        return a quantity computer for a given type
        @param quantity_computer_type: the type
        @param strategy: the strategy
        @return: the computer  
        '''
        if quantity_computer_type == ComputerType.NOMINAL:
            computer = NominalComputer(quantity_computer_type, strategy)
        elif quantity_computer_type == ComputerType.RISK_UNITS:
            computer = UnitsComputer(quantity_computer_type, strategy)

        return computer
    
    def get_financial_instrument(self, instrument):
        '''
        return a financial instrument from a serialized instrument
        @param instrument: the serialized instrument
        @return: a financial instrument 
        '''
        financial_instrument = FinancialInstrument(ticker = instrument['ticker'], name = instrument['name'], 
                                                   asset_class = instrument['asset_class'], currency=instrument['currency'],
                                                   type = instrument['instrument_type'], transactions_fees = instrument['transactions_fees'],
                                                   point_value = instrument['point_value'])
        
        # fill the data_map from instrument data
        for data in instrument['datas']:
            data_date = data['date']
            
            if isinstance(data_date, datetime):
                data_date = data_date.date()
                
            if data['data_type'] == 'CLOSE':
                financial_instrument.set_close_value(data_date, data['value'])
            elif data['data_type'] == 'ADJUSTED_CLOSE':
                financial_instrument.set_adjusted_close_value(data_date, data['value'])
            elif data['data_type'] == 'OPEN':
                financial_instrument.set_open_value(data_date, data['value'])
            elif data['data_type'] == 'HIGH':
                financial_instrument.set_high_value(data_date, data['value'])
            elif data['data_type'] == 'LOW':
                financial_instrument.set_low_value(data_date, data['value'])
            elif data['data_type'] == 'OPEN_INTEREST':
                financial_instrument.set_open_interest(data_date, data['value'])
            elif data['data_type'] == 'VOLUME':
                financial_instrument.set_volume(data_date, data['value'])
            elif data['data_type'] == 'REFERENCE_MONTH':
                financial_instrument.set_reference_month(data_date, data['value'])
            else:
                raise ServerError('No type %s '%data['type'])
                    
        return financial_instrument
    
    def get_computed_strategy(self, backtest_settings):
        '''
        return a time series (net asset value)
        @param backtest_settings: a backtest settings
        @return: the computed strategy
        @raise ServiceError:  
        '''
        
        # initialize strategy
        strategy = Strategy(backtest_settings['name'])
        
        # set dates
        strategy.first_date = datetime.strptime(backtest_settings['first_date'].value, '%Y%m%dT%H:%M:%S').date()
        strategy.last_date = datetime.strptime(backtest_settings['last_date'].value, '%Y%m%dT%H:%M:%S').date()
        
        # set portfolio, first cash flow and currency
        strategy.portfolio = Portfolio(backtest_settings['currency'])
        initial_cash_flow = CashFlow(strategy.first_date,
                                     backtest_settings['amount'],
                                     backtest_settings['currency'])
        strategy.portfolio.add_transaction(initial_cash_flow)
        
        # set rolling
        strategy.rolling = backtest_settings['rolling']
        
        # add instruments
        instruments_cache = {}
        for ticker in backtest_settings['tickers']:
            first_data_date = strategy.calendar_util.get_n_previous_business_date(strategy.first_date, 
                                                                                  backtest_settings['needed_depth'])
            instrument = self.instrument_service.get_by_ticker(ticker, first_data_date, strategy.last_date)
            financial_instrument = self.get_financial_instrument(instrument)
            strategy.add_instrument(financial_instrument) 
    
            # store in cache
            instruments_cache[ticker] = financial_instrument
        
        # add quantity computers
        computers_cache = {}
        for computer_type in backtest_settings['quantity_computers']:
            quantity_computer = self.get_quantity_computer(computer_type, strategy)
            strategy.add_quantity_computer(quantity_computer)
    
            # store in cache
            computers_cache[computer_type] = quantity_computer
        
        # add indicators
        indicators_cache = {}
        for indicator_setting in backtest_settings['indicator_settings']:
            financial_instrument = instruments_cache[indicator_setting['ticker']]
            indicator = self.get_indicator(indicator_setting, backtest_settings, financial_instrument)
            indicator.calendar_util = strategy.calendar_util
            strategy.add_indicator(indicator)
            
            # store in cache
            indicators_cache[indicator.id] = indicator
    
        # add trading blocks
        blocks_cache = {}
        for trading_block_setting in backtest_settings['trading_block_settings']:
            block = TradingBlock(trading_block_setting['name'])
            block.order_type = trading_block_setting['order_type']
            block.instrument = instruments_cache[trading_block_setting['ticker']]
            
            # store in cache
            blocks_cache[block.id] = block
            
            strategy.add_trading_block(block)
            
        # add condition bundle
        for condition_bundle_setting in backtest_settings['condition_bundle_settings']:
            current_block = blocks_cache[condition_bundle_setting['trading_block_name']]
            current_indicator = indicators_cache[condition_bundle_setting['indicator_name']]
            strategy.add_condition_bundle_to_trading_block(current_block,
                                                           condition_bundle_setting['regime_type'],
                                                           current_indicator)
            
        # add quantity computer to blocks
        for quantity_setting in backtest_settings['quantity_settings']:
            current_block = blocks_cache[quantity_setting['trading_block_name']]
            allocation = quantity_setting['allocation']
            current_computer = computers_cache[quantity_setting['quantity_computer_type']]
            strategy.add_quantity_computer_to_trading_block(current_block, current_computer, allocation)
            
        try:    
            strategy.compute()
        except Exception, e:
            raise ServerError(e.message)
        
        # build data to return
        data = []
        
        iterator = strategy.first_date
        
        while iterator <= strategy.last_date:
            a_datetime = datetime(iterator.year,iterator.month,iterator.day)
            line = (a_datetime, strategy.track_record[iterator])
            
            data.append(line)
            
            iterator = strategy.calendar_util.get_next_business_date(iterator)
        
        return data

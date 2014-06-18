'''
Web services which return instrument
@author: julien
'''
from dao.instrument_dao import InstrumentDAO
from dao.market_data_dao import MarketDataDAO
from data.instrument_serialized import InstrumentSerialized
from data.market_data_serialized import MarketDataSerialized
from data_error import DataError
from datetime import datetime, date
from model.market_data import MarketData
from model.meta import Session
from server_error import ServerError
import logging

class InstrumentService(object):
    
    logger = logging.getLogger('InstrumentService')
    
    def __init__(self):
        
        self.__session = Session()
        
        self.__instrument_dao = InstrumentDAO()
    
        self.__market_data_dao = MarketDataDAO()
    
    def market_data_model_to_serialized(self, market_data_model):
        market_data_serialized = MarketDataSerialized()
        market_data_serialized.id = market_data_model.id
        market_data_serialized.value = market_data_model.value
        market_data_serialized.data_type = market_data_model.type
        
        data_date = market_data_model.date
        market_data_serialized.date = datetime(data_date.year, data_date.month, data_date.day)
        
        return market_data_serialized
    
    def instrument_model_to_serialized(self, instrument_model):
        
        # build the serialized object
        instrument_serialized = InstrumentSerialized()
        instrument_serialized.id = instrument_model.id
        instrument_serialized.ticker = instrument_model.ticker
        instrument_serialized.name = instrument_model.name
        instrument_serialized.exchange = instrument_model.exchange
        instrument_serialized.rolling_month = instrument_model.rolling_month
        instrument_serialized.currency = instrument_model.currency
        instrument_serialized.point_value = instrument_model.point_value
        instrument_serialized.transactions_fees = instrument_model.transactions_fees
        instrument_serialized.asset_class = instrument_model.asset_class
        instrument_serialized.instrument_type = instrument_model.type
        instrument_serialized.datas = []
            
        return instrument_serialized

    def get_date(self, a_date):
        # return a date from a datetime if a_date is instance of datetime
        if isinstance(a_date, datetime):
            return a_date.date()
        elif isinstance(a_date, date):
            return a_date
        # return a date from a XML RPC DateTime else
        else:
            return datetime.strptime(a_date.value, '%Y%m%dT%H:%M:%S').date()
    
    def get_by_ticker(self, ticker, first_date, last_date):
        '''
        return an instrument serialized for a given ticker
        @param ticker: the ticker
        @param first_date: the first time series date
        @param last_date: the last time series date 
        @return: the instrument serialized 
        '''
        
        try:
            self.logger.info('Asking data for %s between %s and %s'%(ticker, first_date, last_date))
            # get the model
            model = self.__instrument_dao.get_by_ticker(self.__session, ticker)
        except DataError, e:
            self.logger.error(e.message)
            raise ServerError(e.message)
        
        # convert into serialized object
        if model:
            instrument = self.instrument_model_to_serialized(model)
        
        # fill data
        first_date_converted = self.get_date(first_date)
            
        last_date_converted = self.get_date(last_date)
        
        datas = model.datas.filter(MarketData.date >= first_date_converted).filter(MarketData.date <= last_date_converted)
        
        for market_data in datas:
            self.logger.debug('Appending data %s at %s for %s'%(market_data.type,market_data.date,ticker))
            serialized = self.market_data_model_to_serialized(market_data)
            instrument.datas.append(serialized)
            
        return instrument


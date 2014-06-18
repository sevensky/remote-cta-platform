'''
DAO market data
@author: julien.bernard
'''
from sqlalchemy import func

from data_error import DataError
from model.market_data import MarketData

class MarketDataDAO(object):
    
    def save(self, session, market_data):
        '''
        persist market data
        @param session: sqlalchemy session
        @param market_data: the persisted market data
        @return: the market data 
        '''
        
        try:
            session.add(market_data)
            session.commit()
        except Exception, e:
            session.rollback()
            raise DataError(e.message)
        
        return market_data
    
    
    def delete(self, session, market_data):
        '''
        delete market data
        @param session: sqlalchemy session
        @param market_data: the persisted market data
        '''
        
        try:
            session.delete(market_data)
            session.commit()
        except Exception, e:
            session.rollback()
            raise DataError(e.message)

    def get_by_instrument(self, session, instrument):
        '''
        get market data by instrument
        @param session: sqlalchemy session
        @param instrument: the instrument 
        @return: the data
        '''
        
        try:
            data = session.query(MarketData).filter_by(instrument_id=instrument.id).all()
        except Exception, e:
            raise DataError(e.message)
        
        return data
    
    def get_data(self, session, instrument, date, type):
        '''
        get market datum by instrument type and date
        @param session: sqlalchemy session
        @param instrument: the instrument
        @param date: the date
        @param type: the type  
        '''
        try:
            data = session.query(MarketData).filter_by(instrument_id=instrument.id,
                                                       date=date, type=type).first()
        except Exception, e:
            raise DataError(e.message)
        
        return data
        

    def get_last_date(self, session, instrument):
        '''
        get the last date for a given instrument
        @param session: sqlalchemy session
        @param instrument: the instrument  
        '''
        try:
            last_date = session.query(func.max(MarketData.date)).filter_by(instrument_id=instrument.id).first()
        except Exception, e:
            raise DataError(e.message)
        
        return last_date[0]
'''
DAO instrument
@author: julien.bernard
'''
from model.instrument import Instrument
from data_error import DataError


class InstrumentDAO(object):
    
    def save(self, session, instrument):
        ''' 
        persist an instrument 
        @param instrument: instrument to persist
        @param session: sqlalchemy session  
        @return: the persited instrument
        '''
        
        try:
            session.add(instrument)
            session.commit()
        except Exception, e:
            session.rollback()
            raise DataError(e.message)
            
        return instrument
    
    def delete(self, session, instrument):
        ''' 
        delete an instrument 
        @param instrument: instrument to delete 
        @param session: sqlalchemy session
        '''
        
        try:
            session.delete(instrument)
            session.commit()
        except Exception, e:
            session.rollback()
            raise DataError(e.message)
    
    def get_by_ticker(self, session, ticker):
        '''
        reach an instrument with its ticker
        @param ticker: the ticker string
        @param session: sqlalchemy session
        @return: the instrument or none if ticker does not exist
        '''
        
        instrument = None
        try:
            instrument = session.query(Instrument).filter_by(ticker=ticker).first()
        except Exception, e:
            raise DataError(e.message)
        
        return instrument
            
    def get_by_tickers(self, session, tickers):
        '''
        reach a list of instruments given their tickers
        @param tickers: list of tickers 
        @param session: sqlalchemy session
        @return: the instrument list 
        '''    
        instruments = []
        try:
            instruments = session.query(Instrument).filter(Instrument.ticker.in_(tickers))
        except Exception, e:
            raise DataError(e.message)

        return instruments
    
    def get_all(self, session):
        '''
        get all instruments in database
        @param session: sqlalchemy session
        @return: the list of instruments
        '''
        instrument = None
        try:
            instrument = session.query(Instrument).all()
        except Exception, e:
            raise DataError(e.message)
        
        return instrument
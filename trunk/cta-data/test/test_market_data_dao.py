'''
Created on 8 juin 2011

@author: julien.bernard
'''
import unittest

from model.meta import Base, Session
from model.market_data import MarketData
from datetime import date
from model.instrument import Instrument
from dao.instrument_dao import InstrumentDAO
from dao.market_data_dao import MarketDataDAO

class TestMarketDataDAO(unittest.TestCase):
    
    session = Session()
    value = 10.0
    date = date(2000,1,1)
    type = 'MyType'
    ticker = 'MyTicker'
    name = 'MyName'

    instrument = Instrument()
    instrument.name = name
    instrument.ticker = ticker
        
    
            
    def setUp(self):
        Base.metadata.create_all()
        
        instrument_dao = InstrumentDAO()
        instrument_dao.save(self.session, self.instrument)

    def tearDown(self):
        Base.metadata.drop_all()

    def testDAO(self):
        data = MarketData()
        data.type = self.type
        data.value = self.value
        data.date = self.date
        data.instrument = self.instrument
        
        market_data_dao = MarketDataDAO()
        
        # test save
        market_data_dao.save(self.session, data)
        self.assertNotEqual(data.id, None, 'market data id')
        self.assertEqual(data.type, self.type, 'market data type')
        self.assertEqual(data.value, self.value, 'market data value')
        self.assertEqual(data.date, self.date, 'market data date')
        self.assertEqual(data.instrument_id, self.instrument.id, 'market data type')
        
        # test get by instrument
        new_data = market_data_dao.get_by_instrument(self.session, self.instrument)
        self.assertEqual(new_data[0].id, data.id, 'both ids equals')
        
        last_date = market_data_dao.get_last_date(self.session, self.instrument)
        self.assertEqual(last_date, data.date)
        # test delete
        market_data_dao.delete(self.session, data)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDAO']
    unittest.main()
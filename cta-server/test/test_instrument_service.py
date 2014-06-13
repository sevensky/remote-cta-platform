import unittest
from datetime import datetime
from model.instrument import Instrument
from model.market_data import MarketData
from model.data_type import DataType
from model.meta import Session, Base
from dao.instrument_dao import InstrumentDAO
from dao.market_data_dao import MarketDataDAO
from instrument_service import InstrumentService


class TestInstrumentService(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all()

        instrument = Instrument()
        instrument.ticker = 'MyTicker'
        instrument.asset_class = 'MyAssetClass'
        instrument.name = 'MyName'
        instrument.currency = 'USD'
        instrument.type = 'MyType'
        instrument.transactions_fees = 0.
        instrument.point_value = 1
        instrument.exchange = 'MyExchange'
        instrument.rolling_month = 'H'
        
        market_data = MarketData()
        market_data.instrument = instrument
        market_data.type = DataType.CLOSE
        market_data.date = datetime(2000,1,3)
        market_data.value = 100.
        
        session = Session()
        
        instrument_dao = InstrumentDAO()
        instrument_dao.save(session, instrument)
        
        market_data_dao = MarketDataDAO()
        market_data_dao.save(session, market_data)
        
        self.instrument_service = InstrumentService() 

    def tearDown(self):
        Base.metadata.drop_all()


    def testGetByTicker(self):
        
        instrument_serialized = self.instrument_service.get_by_ticker('MyTicker', datetime(1970,1,1), datetime(2030,1,1))
        
        self.assertEqual(instrument_serialized.ticker, 'MyTicker', 'good ticker')
        self.assertEqual(instrument_serialized.datas[0].value, 100., 'good market data value')
        
        instrument_serialized = self.instrument_service.get_by_ticker('MyTicker', datetime(2001,1,1), datetime(2030,1,1))
        self.assertEqual(len(instrument_serialized.datas), 0, 'empty market data')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
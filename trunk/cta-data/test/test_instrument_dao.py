'''
@author: julien.bernard
'''
from dao.instrument_dao import InstrumentDAO
from model.instrument import Instrument
import unittest
from model.meta import Base, Session


class TestInstrumentDAO(unittest.TestCase):

    ticker = 'MyTicker'
    name = 'MyName'
    session = Session()

    def setUp(self):
        Base.metadata.create_all()
        
    def tearDown(self):
        Base.metadata.drop_all()

    def testDAO(self):
        instrument = Instrument()
        instrument.ticker = self.ticker
        instrument.name = self.name
        
        dao = InstrumentDAO()
        
        # test save
        dao.save(self.session, instrument)
        self.assertEqual(instrument.name, self.name, 'instrument name')
        self.assertEqual(instrument.ticker, self.ticker, 'instrument ticker')
        self.assertNotEqual(instrument.id, None, 'instrument id')
        
        # test update
        id = instrument.id
        instrument.name = 'NewName'
        dao.save(self.session, instrument)
        self.assertNotEqual(instrument.name, self.name, 'not instrument name')
        self.assertEqual(instrument.name, 'NewName', 'new instrument name')
        self.assertEqual(instrument.ticker, self.ticker, 'old instrument ticker')
        self.assertEqual(instrument.id, id, 'old instrument id')
        
        # test get by ticker
        new_instrument = dao.get_by_ticker(self.session, self.ticker)
        self.assertEqual(instrument.id, new_instrument.id, 'both ids equals')
        
        self.assertEqual(dao.get_by_ticker(self.session, 'WrongTicker'),None, 'None object for wrong ticker')
        
        # test delete
        dao.delete(self.session, instrument)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
Created on 1 juil. 2011

@author: julien.bernard
'''
import unittest
from numpy import cos, arctan
from backtest.indicator.digital_filter_indicator import DigitalFilterIndicator
from backtest.indicator.building_type import BuildingType
from backtest.indicator.indicator_type import IndicatorType
from backtest.indicator.regime import Regime

class MockInstrument(object):
    
    def get_adjusted_close_value(self, date):
        return cos(8*arctan(1)/30*date) + cos(8*arctan(1)/4*date)
    
class MockCalendarUtil(object):
    
    def get_n_previous_business_date(self, date, n):
        return date - n
    
    def get_previous_business_date(self, date):
        return date - 1
    
    def get_previous_quote_date(self, date, instrument):
        return date - 1
    
    def get_n_previous_quote_date(self, date, instrument, n):
        return date - n
     
    def get_next_business_date(self, date):
        return date + 1
    
    def get_next_quote_date(self, date, instrument):
        return date + 1

class TestDigitalFilterIndicator(unittest.TestCase):


    def testGetRegime(self):
        instrument = MockInstrument()
        # test one line value Butterworth
        indicator = DigitalFilterIndicator('ID', IndicatorType.BUTTERWORTH, BuildingType.ONE_LINE_VALUE, instrument, [30])
        indicator.calendar_util = MockCalendarUtil()
        
        self.assertEqual(indicator.get_regime(336),Regime.BULL,'butterworth bull')
        
        indicator.last_update = None
        self.assertEqual(indicator.get_regime(335),Regime.BEAR,'butterworth bear')
        
        # test one line Bessel
        indicator = DigitalFilterIndicator('ID', IndicatorType.BESSEL, BuildingType.ONE_LINE_VALUE, instrument, [30])
        indicator.calendar_util = MockCalendarUtil()
        
        self.assertEqual(indicator.get_regime(326),Regime.BEAR,'bessel bear')
        
        indicator.last_update = None
        self.assertEqual(indicator.get_regime(327),Regime.BULL,'bessel bull')
        
        # test one line Chebyschev
        indicator = DigitalFilterIndicator('ID', IndicatorType.CHEBYSCHEV, BuildingType.ONE_LINE_VALUE, instrument, [30])
        indicator.calendar_util = MockCalendarUtil()
        
        self.assertEqual(indicator.get_regime(319),Regime.BULL,'chebyshev bull')
        
        indicator.last_update = None
        self.assertEqual(indicator.get_regime(318),Regime.BEAR,'chebyschev bear')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetRegime']
    unittest.main()
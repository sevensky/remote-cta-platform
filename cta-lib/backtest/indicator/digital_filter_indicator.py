'''
Implementation of Butterworth filter as trading indicator
@author: julien.bernard
'''
from backtest.indicator.abstract_indicator import AbstractIndicator
from core_error import CoreError
from backtest.indicator.building_type import BuildingType
from backtest.indicator.regime import Regime
from finance.math.digital_filter import DigitalFilter
from backtest.indicator.regime_helper import RegimeHelper
from backtest.indicator.indicator_type import IndicatorType
import logging

class DigitalFilterIndicator(AbstractIndicator):
    
    logger = logging.getLogger('DigitalFilterIndicator')
    
    def __init__(self, id, indicator_type, building_type, instrument, parameters):
        AbstractIndicator.__init__(self, id, indicator_type, building_type, instrument, parameters)
        
        self.cache = {}
    
    def _initilialize(self, date):
        
        iterator_date = self.calendar_util.get_n_previous_quote_date(date, self.instrument, 300)
        
        # initialize last update
        self.last_update = iterator_date
        
        while iterator_date < date:
            self.get_regime(iterator_date) 
            iterator_date = self.calendar_util.get_next_quote_date(iterator_date, self.instrument)
    
    def _get_regime_one_line(self, date, date_1, date_2):
        
        # check parameters
        if len(self.parameters) != 1:
            raise CoreError('Error in parameter')
        
        # build the cache
        if 'line' not in self.cache:
            self.cache['line'] = []
        
        # check the cache
        if len(self.cache['line']) < 2:
            self.cache['line'].insert(0, self.instrument.get_adjusted_close_value(date))
            return Regime.FLAT
        
        # get filter input values
        current_value = self.instrument.get_adjusted_close_value(date)
        last_value = self.instrument.get_adjusted_close_value(date_1)
        before_value = self.instrument.get_adjusted_close_value(date_2)
        last_filter = self.cache['line'][0]
        before_filter = self.cache['line'][1]
        
        # compute filter
        if self.indicator_type == IndicatorType.BUTTERWORTH:
            current_filter = DigitalFilter.get_butterworth_lpf_value(self.parameters[0], current_value, last_value, before_value, last_filter, before_filter)
        elif self.indicator_type == IndicatorType.BESSEL:
            current_filter = DigitalFilter.get_bessel_lpf_value(self.parameters[0], current_value, last_value, before_value, last_filter, before_filter)
        elif self.indicator_type == IndicatorType.CHEBYSCHEV:
            current_filter = DigitalFilter.get_chebyschev_lpf_value(self.parameters[0], current_value, last_value, before_value, last_filter, before_filter)
        
        if self.building_type == BuildingType.ONE_LINE_SLOPE:
            slope = current_filter - last_filter
            current_regime = RegimeHelper.get_regime(self.building_type, date, line=slope)
        elif self.building_type == BuildingType.ONE_LINE_VALUE:
            current_regime = RegimeHelper.get_regime(self.building_type, date, line=current_filter, 
                                                     instrument=self.instrument.get_adjusted_close_value(date))
        
        # update cache
        self.cache['line'].pop()
        self.cache['line'].insert(0, current_filter)
        
        return current_regime
    
    
    def get_regime(self, date):
        '''
        get the date regime
        @param date: the date
        @return: the regime
        @raise CoreError: 
        '''
        try:
            # check if initialization is needed
            if self.last_update == None:
                self._initilialize(date)
        
            # check if last update is before date then raise an exception
            if date < self.last_update:
                raise CoreError('%s is before the last update date %s' % (date, self.last_update))
        
            # check if date is the last update date to return last regime
            if self.last_update == date:
                return self.last_regime
        
            # t-1 and t-2
            date_1 = self.calendar_util.get_previous_quote_date(date, self.instrument)
            date_2 = self.calendar_util.get_previous_quote_date(date_1, self.instrument)
        
            if self.building_type in [BuildingType.ONE_LINE_SLOPE,BuildingType.ONE_LINE_VALUE]:
                self.last_regime = self._get_regime_one_line(date, date_1, date_2)
            else:
                raise NotImplementedError('building type %s not yet implemented' % self.building_type)
        
            # update last update
            self.last_update = date
        
            return self.last_regime
        except Exception, e:
            raise CoreError('Error on %s at date %s: %s'%(self.instrument.get_ticker(),date,e.message))
        
        

'''
Simple moving average
@author: julien.bernard
'''
import numpy

from backtest.indicator.abstract_indicator import AbstractIndicator
from core_error import CoreError
from backtest.indicator.building_type import BuildingType
from backtest.indicator.regime import Regime
from backtest.indicator.regime_helper import RegimeHelper

class Sma(AbstractIndicator):
    
    def __init__(self, id, indicator_type, building_type, instrument, parameters):
        AbstractIndicator.__init__(self, id, indicator_type, building_type, instrument, parameters)
        
        self.cache = {}
    
    def _initilialize(self, date):
        
        iterator_date = self.calendar_util.get_previous_quote_date(date, self.instrument)
        
        # initialize last update
        self.last_update = iterator_date
        
        self.get_regime(iterator_date) 
    
    def _get_first_filter(self, date):
        # compute the first moving average
        first_date = self.calendar_util.get_n_previous_quote_date(n=self.parameters[0]-1,
                                                                      date=date,
                                                                      instrument=self.instrument)
        prices = []
        while first_date <= date:
            prices.append(self.instrument.get_adjusted_close_value(first_date))
            first_date = self.calendar_util.get_next_quote_date(date=date,
                                                                instrument=self.instrument)
        return numpy.mean(prices)
    
    def _get_current_filter(self, date):
        # get filter input values
        current_value = self.instrument.get_adjusted_close_value(date)
        past_date = self.calendar_util.get_n_previous_quote_date(n=self.parameters[0],
                                                                 date=date,
                                                                 instrument=self.instrument)
        past_value = self.instrument.get_adjusted_close_value(past_date)
        last_filter = self.cache['line'][0]
        
        # compute filter
        current_filter = last_filter + (current_value - past_value) / self.parameters[0]
        
        return current_filter
    
    def _get_regime_one_line(self, date):
        # check parameters
        if len(self.parameters) != 1:
            raise CoreError('Error in parameter')
        
        # build the cache
        if 'line' not in self.cache:
            self.cache['line'] = []
        
        # check the cache
        if len(self.cache['line']) < 1:
            # compute the first moving average
            current_filter = self._get_first_filter(date)
            self.cache['line'].insert(0, current_filter)
            return Regime.FLAT
        
        # compute filter
        current_filter = self._get_current_filter(date)
        
        if self.building_type == BuildingType.ONE_LINE_SLOPE:
            slope = current_filter - self.cache['line'][0]
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
        
            if self.building_type in [BuildingType.ONE_LINE_SLOPE,BuildingType.ONE_LINE_VALUE]:
                self.last_regime = self._get_regime_one_line(date)
            else:
                raise NotImplementedError('building type %s not yet implemented' % self.building_type)
        
            # update last update
            self.last_update = date
        
            return self.last_regime
        except Exception, e:
            raise CoreError('Error on %s at date %s: %s'%(self.instrument.get_ticker(),date,e.message))
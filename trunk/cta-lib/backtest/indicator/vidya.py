'''
Chandle dynamic moving average
'''
import numpy
from backtest.indicator.abstract_indicator import AbstractIndicator
from core_error import CoreError
from backtest.indicator.building_type import BuildingType
from backtest.indicator.regime import Regime
from backtest.indicator.regime_helper import RegimeHelper


class Vidya(AbstractIndicator):
    
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
    
    
    
    def _get_alpha(self, date, depth, historical_depth):
        
        # specific cache keys for vidya computation
        historical_key = 'historical_prices_%i'%depth
        normal_key = 'normal_prices_%i'%depth
        
        # check if there are some data in cache
        if historical_key not in self.cache:
            self.cache[historical_key] = []
        
        if normal_key not in self.cache:
            self.cache[normal_key] = []
        
        # check if cache is empty then fill it
        if len(self.cache[historical_key]) == 0:
            # get the date related to historical depth
            historical_date = self.calendar_util.get_n_previous_quote_date(date=date,
                                                                           instrument=self.instrument,
                                                                           n=historical_depth)
        
            # get the date related to depth
            normal_date = self.calendar_util.get_n_previous_quote_date(date=date,
                                                                       instrument=self.instrument,
                                                                       n=depth)
        
            iterator_date = historical_date
        
            # fill list of prices before computing standard deviation
            historical_prices = []
            normal_prices = []
        
            while iterator_date <= date:
                value = self.instrument.get_adjusted_close_value(iterator_date)
            
                if iterator_date >= normal_date:
                    normal_prices.append(value)
                historical_prices.append(value)
            
                iterator_date = self.calendar_util.get_next_quote_date(instrument=self.instrument,
                                                                       date=iterator_date)
                
            self.cache[historical_key] = historical_prices
            self.cache[normal_key] = normal_prices
                
        # use cache to compute standard deviation
        else:
            self.cache[historical_key].pop()
            self.cache[normal_key].pop()
            self.cache[historical_key].insert(0, self.instrument.get_adjusted_close_value(date))
            self.cache[normal_key].insert(0, self.instrument.get_adjusted_close_value(date))
        
        normal_sd = numpy.std(self.cache[normal_key])
        historical_sd = numpy.std(self.cache[historical_key])
        
        return 2./(depth+1.)*(normal_sd/historical_sd)
                
    
    
    def _get_regime_one_line(self, date):
        # check parameters
        if len(self.parameters) != 2:
            raise CoreError('Error in parameter')
        
        # build the cache
        if 'line' not in self.cache:
            self.cache['line'] = []
        
        # check the cache
        if len(self.cache['line']) < 1:
            self.cache['line'].insert(0, self.instrument.get_adjusted_close_value(date))
            return Regime.FLAT
        
        # get filter input values
        current_value = self.instrument.get_adjusted_close_value(date)
        last_filter = self.cache['line'][0]
        
        # compute filter
        current_alpha = self._get_alpha(date, self.parameters[0], int(self.parameters[0]*self.parameters[1]))
        current_filter = current_alpha*current_value + (1.-current_alpha)*last_filter

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
        
            if self.building_type in [BuildingType.ONE_LINE_SLOPE,BuildingType.ONE_LINE_VALUE]:
                self.last_regime = self._get_regime_one_line(date)
            else:
                raise NotImplementedError('building type %s not yet implemented' % self.building_type)
        
            # update last update
            self.last_update = date
        
            return self.last_regime
        except Exception, e:
            raise CoreError('Error on %s at date %s: %s'%(self.instrument.get_ticker(),date,e.message))
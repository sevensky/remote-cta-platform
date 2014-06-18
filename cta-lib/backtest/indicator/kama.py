'''
Kaufman moving average
'''
from backtest.indicator.abstract_indicator import AbstractIndicator
from core_error import CoreError
from backtest.indicator.building_type import BuildingType
from backtest.indicator.regime import Regime
from backtest.indicator.regime_helper import RegimeHelper
from finance.math.efficient_ratio import EfficientRatio

class Kama(AbstractIndicator):
    fast_ratio = 2./(2.+1.) 
    
    slow_ratio = 2./(30.+1.)
    
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
    
    
    def _get_alpha(self, date, depth):
        er = EfficientRatio.get_value(self.instrument, date, depth, self.calendar_util)
        return (er*(self.fast_ratio-self.slow_ratio)+self.slow_ratio)**2
    
    
    def _get_regime_one_line(self, date):
        # check parameters
        if len(self.parameters) != 1:
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
        current_alpha = self._get_alpha(date, self.parameters[0])
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
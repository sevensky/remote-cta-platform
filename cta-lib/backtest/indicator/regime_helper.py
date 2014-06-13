'''
Helper for regime in function of building type indicator
@author: julien.bernard
'''
from core_error import CoreError
from backtest.indicator.building_type import BuildingType
from backtest.indicator.regime import Regime

# TODO: unit tests
class RegimeHelper(object):
    
    @staticmethod
    def get_regime(building_type, date, **kwargs):
        '''
        return the regime in function of building indicator type
        @return: the regime
        @raise CoreError:
        '''
        try:
            if building_type == BuildingType.TWO_LINES_VALUE or building_type == BuildingType.TWO_LINES_SLOPE:
                # get the line value or slope from args
                short_line = kwargs['short_line']
                long_line = kwargs['long_line']
                
                # return the regime
                if short_line > long_line:
                    return Regime.BULL
                else:
                    return Regime.BEAR
                
            elif building_type == BuildingType.ONE_LINE_VALUE:
                # get the line value or slope from args
                line = kwargs['line']
                instrument = kwargs['instrument']
                
                # return the regime
                if instrument > line:
                    return Regime.BULL
                else:
                    return Regime.BEAR
            elif building_type == BuildingType.ONE_LINE_SLOPE:
                line = kwargs['line']
                
                if line > 0:
                    return Regime.BULL
                else:
                    return Regime.BEAR
                 
            else:
                raise NotImplementedError('other building type are not yet implemented')
        except Exception, e:
            raise CoreError(e.message)

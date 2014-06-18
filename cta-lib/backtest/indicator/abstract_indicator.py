'''
Abstract class for indicator, contains indicator type too
@author: julien.bernard
'''

class AbstractIndicator(object):

    def __init__(self, id, indicator_type, building_type, instrument, parameters):
        self.id = id
        
        self.building_type = building_type
        
        self.indicator_type = indicator_type
        
        self.instrument = instrument
        
        self.parameters = parameters
        
        self.calendar_util = None
    
        self.last_update = None
        
        self.last_regime = None
        
    def __repr__(self):
        return self.id

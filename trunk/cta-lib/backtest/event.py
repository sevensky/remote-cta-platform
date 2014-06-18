'''
Event class contains a type and a data dict
@author: julien.bernard
'''

class Event(object):
    
    # list of events type
    VALORIZATION_EVENT = 'VALORIZATION_EVENT'
    SIGNALS_EVENT = 'SIGNALS_EVENT'
    ROLLING_EVENT = 'ROLLING_EVENT'
    TRADE_EVENT = 'TRADE_EVENT'
    TRADING_TIME_EVENT = 'TRADING_TIME_EVENT'
    
    def __init__(self, event_type):
        self.type = event_type
        
        self.datas = {}
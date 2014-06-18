'''
Business class which modelizes all financial instruments
@author: julien
'''
from core_error import CoreError
from finance.data_type import DataType
from finance.instrument_type import InstrumentType

class FinancialInstrument(object):
    
    def __init__(self, ticker, name, asset_class, currency, type, transactions_fees, point_value):
        self.ticker = ticker
        self.name = name
        self.asset_class = asset_class
        self.currency = currency
        self.type = type
        self.transactions_fees = transactions_fees
        self.point_value = point_value
        self.__close_map = {}
        self.__adj_close_map = {}
        self.__open_map = {}
        self.__high_map = {}
        self.__low_map = {}
        self.__open_interest_map = {}
        self.__volume_map = {}
        self.__reference_month_map = {}

    def get_close_value(self, date):
        '''
        return the instrument close value at a date
        @param date: the date
        @return: the value 
        '''
        if date in self.__close_map:
            return self.__close_map[date]
    
    def set_close_value(self, date, value):
        '''
        set a given data at a date
        @param date: the date
        @param value: the value  
        '''
        self.__close_map[date] = value
        
    def get_adjusted_close_value(self, date):
        '''
        return the instrument adjusted close value at a date
        @param date: the date
        @return: the value 
        '''
        if date in self.__adj_close_map:
            return self.__adj_close_map[date]
        
    def set_adjusted_close_value(self, date, value):
        '''
        set a given data at a date
        @param date: the date
        @param value: the value  
        '''
        self.__adj_close_map[date] = value
        
    def get_open_value(self, date):
        '''
        return the instrument open value at a date
        @param date: the date
        @return: the value 
        '''
        if date in self.__open_map:
            return self.__open_map[date]

    def set_open_value(self, date, value):
        '''
        set a given data at a date
        @param date: the date
        @param value: the value  
        '''
        self.__open_map[date] = value
        
    def get_high_value(self, date):
        '''
        return the instrument high value at a date
        @param date: the date
        @return: the value 
        '''
        if date in self.__high_map:
            return self.__high_map[date]
    
    def set_high_value(self, date, value):
        '''
        set a given data at a date
        @param date: the date
        @param value: the value  
        '''
        self.__high_map[date] = value    
    
    def get_low_value(self, date):
        '''
        return the instrument low value at a date
        @param date: the date
        @return: the value 
        '''
        if date in self.__low_map:
            return self.__low_map[date]

    def set_low_value(self, date, value):
        '''
        set a given data at a date
        @param date: the date
        @param value: the value  
        '''
        self.__low_map[date] = value

    def get_volume(self, date):
        '''
        return the instrument volume at a date
        @param date: the date
        @return: the volume
        '''
        if date in self.__volume_map:
            return self.__volume_map[date]

    def set_volume(self, date, value):
        '''
        set a given data at a date
        @param date: the date
        @param value: the value  
        '''
        self.__volume_map[date] = value

    def get_open_interest(self, date):
        '''
        return the instrument open interest at a date
        @param date: the date
        @return: the open interest
        '''
        
        if date in self.__open_interest_map:
            return self.__open_interest_map[date]

    def set_open_interest(self, date, value):
        '''
        set a given data at a date
        @param date: the date
        @param value: the value  
        '''
        self.__open_interest_map[date] = value

    def get_reference_month(self, date):
        '''
        return the reference month at a given date
        @param date: the date
        @return: the reference month
        '''
        if date in self.__reference_month_map:
            return self.__reference_month_map[date] 
        
    def set_reference_month(self, date, value):
        '''
        set a given data at a date
        @param date: the date
        @param value: the value  
        '''
        self.__reference_month_map[date] = value
        
    def is_need_cash(self):
        '''
        return true if you pay cash to trade instrument
        @return: true or false
        '''
        if self.get_type() == InstrumentType.FUTURE:
            return False
        
        return True
    
    def get_currency(self):
        '''
        return the instrument currency
        @return: the currency
        '''
        return self.currency
    
    def get_name(self):
        '''
        return the instrument name
        @return: the name
        '''
        return self.name
    
    def get_asset_class(self):
        '''
        return the asset class
        @return: return the instrument asset class
        '''
        return self.asset_class
    
    def get_ticker(self):
        '''
        return instrument ticker
        @return: the ticker
        '''
        return self.ticker
    
    def get_type(self):
        '''
        return instrument type
        @return: the instrument type
        '''
        return self.type
    
    def get_transactions_fees(self):
        '''
        return the transations fees 
        @return: the transactions fees
        '''
        return self.transactions_fees
    
    def get_point_value(self):
        '''
        return the point value
        '''
        return self.point_value
    
    def get_first_quote_date(self):
        '''
        return the first quote date
        @return: the date
        '''
        return min(self.__adj_close_map.keys())
    
    def get_last_quote_date(self):
        '''
        return the first quote date
        @return: the date
        '''
        return max(self.__adj_close_map.keys())
    
    def __repr__(self):
        return self.get_name()
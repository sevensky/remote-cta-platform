'''
Class which map data model and serialized object for web services
@author: julien
'''
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import Integer, String, Float, Array
from data.market_data_serialized import MarketDataSerialized

class InstrumentSerialized(ClassSerializer):
    
    class types:
        id = Integer
        ticker = String
        name = String
        exchange = String
        rolling_month = String
        currency = String
        point_value = Float
        transactions_fees = Float
        asset_class = String
        instrument_type = String
        datas = Array(MarketDataSerialized)

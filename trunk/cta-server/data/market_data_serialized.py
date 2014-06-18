'''
Class which map data model and serialized object for web services
@author: julien
'''
from soaplib.serializers.clazz import ClassSerializer
from soaplib.serializers.primitive import Integer, Float, DateTime, String

class MarketDataSerialized(ClassSerializer):
    
    class types:
        
        id = Integer
        value = Float
        date = DateTime
        data_type = String

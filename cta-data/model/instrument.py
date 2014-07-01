'''
Instrument model, application data such as contract specifications

@author: julien.bernard
'''

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relation
from model.meta import Base

class Instrument(Base):
    
    __tablename__ = 't_instruments'
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False, unique=True)
    exchange = Column(String(50))
    rolling_month = Column(String(12))
    currency = Column(String(3))
    point_value = Column(Float)
    transactions_fees = Column(Float)
    asset_class = Column(String(50))
    type = Column(String(50))
    datas = relation("MarketData", backref="ins", order_by="MarketData.date", lazy="dynamic")
    
    def __repr__(self):
        return self.name
    
    def __eq__(self, other):
        return isinstance(other, Instrument) and self.id == other.id
     
    def __hash__(self):
        return hash(id)

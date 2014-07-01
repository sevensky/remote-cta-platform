'''
Data model, attached to an instrument, represent price, volume, open interest time series

@author: julien.bernard
'''
from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from sqlalchemy.orm import relation
from model.instrument import Instrument
from model.meta import Base
from sqlalchemy.schema import UniqueConstraint

class MarketData(Base):
    
    __tablename__ = 't_market_datas'
    __table_args__ = (UniqueConstraint('date','type','instrument_id'), {})
    
    id = Column(Integer, primary_key=True)
    value = Column(Float,nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String(20), nullable=False)
    instrument_id = Column(Integer, ForeignKey('t_instruments.id'))
    instrument = relation(Instrument, primaryjoin=instrument_id==Instrument.id)
        
    def __repr__(self):
        return '%s %s %s %s'%(self.instrument, self.date,str(self.value),self.type)

    def __eq__(self, other):
        return isinstance(other, MarketData) and self.id == other.id
     
    def __hash__(self):
        return hash(id)
    
    
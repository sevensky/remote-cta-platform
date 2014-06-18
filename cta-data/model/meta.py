'''
SQLAlchemy object session and base

@author: julien.bernard
'''
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
import settings

if settings.db_engine == 'mysql':
    engine = create_engine('%s://%s:%s@%s:%s/%s'%(settings.db_engine,
                                                  settings.user,
                                                  settings.password,
                                                  settings.host,
                                                  settings.port,
                                                  settings.db_name))
else:
    engine = create_engine('sqlite:///cta.db')

Session = sessionmaker(bind=engine)

Base = declarative_base(bind=engine)
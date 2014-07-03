'''
Script which create fill instrument table from a text file downloaded on the web

@author: julien.bernard
'''

import csv
import urllib2
import logging
from datetime import date
import time
from zipfile import ZipFile
from model.instrument_type import InstrumentType
from model.market_data import MarketData
from model.data_type import DataType
from model.meta import Session
from dao.instrument_dao import InstrumentDAO
from dao.market_data_dao import MarketDataDAO


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('InstrumentFiller')

data_repository = '/home/julien/Data/'

session = Session()
instrument_dao = InstrumentDAO()
market_data_dao = MarketDataDAO()

def _get_remote_response(url):
    try:
        response = urllib2.urlopen(url)
    except urllib2.URLError, e:
        logger.error(e)
            
    return response
    

def _download_file(url, file_name):
    response = _get_remote_response(url)
            
    data_file = file(file_name,'w')
    
    try:
        data_file.write(response.read())
    except IOError, e:
        logger.error(e)
    finally:
        response.close()
        data_file.close()

def _download_zip(url, file_name):
    response = _get_remote_response(url)
    
    content = ''
    
    while 1:
        data = response.read()
        if not data:
            break
        content += data
        
    data_file = file(file_name,'wb')
    
    try:
        data_file.write(content)
    except IOError, e:
        logger.error(e)
    finally:
        response.close()
        data_file.close()

def _fill_market_data(file_name, instrument):
    reader = csv.reader(open(file_name, 'r'))

    data_list = []
    
    for row in reader:
        # set the current_date from string
        t = time.strptime(row[0], '%Y%m%d')
        current_date = date(t.tm_year, t.tm_mon, t.tm_mday)
        
        # open
        open_price = MarketData()
        open_price.value = float(row[1])
        open_price.instrument = instrument
        open_price.type = DataType.OPEN
        open_price.date = current_date
        data_list.append(open_price)
        
        # high
        high = MarketData()
        high.value = float(row[2])
        high.instrument = instrument
        high.type = DataType.HIGH
        high.date = current_date
        data_list.append(high)
        
        # low
        low = MarketData()
        low.value = float(row[3])
        low.instrument = instrument
        low.type = DataType.LOW
        low.date = current_date
        data_list.append(low)
        
        # adj close
        adj_close = MarketData()
        adj_close.value = float(row[4])
        adj_close.instrument = instrument
        adj_close.type = DataType.ADJUSTED_CLOSE
        adj_close.date = current_date
        data_list.append(adj_close)
        
        # volume
        volume = MarketData()
        volume.value = float(row[5])
        volume.instrument = instrument
        volume.type = DataType.VOLUME
        volume.date = current_date
        data_list.append(volume)
        
        # open interest
        open_interest = MarketData()
        open_interest.value = float(row[6])
        open_interest.instrument = instrument
        open_interest.type = DataType.OPEN_INTEREST
        open_interest.date = current_date
        data_list.append(open_interest)
        
        # reference month
        reference_month = MarketData()
        reference_month.value = int(row[7])
        reference_month.instrument = instrument
        reference_month.type = DataType.REFERENCE_MONTH
        reference_month.date = current_date
        data_list.append(reference_month)
        
        # close
        close = MarketData()
        close.value = float(row[8])
        close.instrument = instrument
        close.type = DataType.CLOSE
        close.date = current_date
        data_list.append(close)
        
    market_data_dao.save_all(session, data_list)
        
def _unzip_file(file_name):
    zip_file = ZipFile(file_name)
    
    zip_file.extractall(path=data_repository)
    
    zip_file.close()
        
if __name__ == "__main__":
    
    logger.info('Instrument filling starting ...')
    
    try:
        # download trading blox dictionary futures data_file
        _download_file(url='http://www.tradingblox.com/tradingblox/CSIUA/FuturesInfo.txt',
                         file_name = data_repository + '/FuturesInfo.txt')
    
        # dowload time series zip file
        _download_zip(url='http://www.tradingblox.com/Data/DataOnly.zip',
                        file_name = data_repository + '/DataOnly.zip')
    
        # unzip the time series zip file
        _unzip_file(file_name = data_repository + '/DataOnly.zip')
    
        # read the dictionary file and persist instrument field into database
        content = csv.reader(open(data_repository + '/FuturesInfo.txt', 'r'))
    
        for row in content:
        
            # load instrument from database if none then no treatment
            instrument = instrument_dao.get_by_ticker(session, row[0])
        
            if instrument:
                logger.info('Filling %s'%instrument.name)
                # the exchange in caps
                instrument.exchange = row[4].upper()
                # the rolling month chain in caps
                instrument.rolling_month = row[5].upper()
                # the currency in caps
                instrument.currency = row[7].upper()
                # the point size manage case where number are given with coma (ex: 1,000.00)
                instrument.point_value = float(row[8].replace(',',''))
                # type
                instrument.type = InstrumentType.FUTURE
                # persit and fill instrument model
                instrument_dao.save(session, instrument)
                # add market data
                _fill_market_data(data_repository + '/Futures/' + row[3], instrument)
                
    except Exception, e:
        logger.error(e.message)
            
    logger.info('End of instrument filling')
        
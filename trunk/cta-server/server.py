#!/usr/bin/python
'''
The server code
@author: julien
'''
import sys
import logging

sys.path.append('/home/julien/server/cta-data')
sys.path.append('/home/julien/server/cta-lib')
sys.path.append('/home/julien/server/cta-server')

from SimpleXMLRPCServer import SimpleXMLRPCServer

from backtest_service import BacktestService

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO)
    
    server = SimpleXMLRPCServer(('0.0.0.0', 8080))
    server.register_introspection_functions()
    
    server.register_instance(BacktestService())
    
    server.serve_forever()

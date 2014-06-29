import xmlrpclib
from datetime import datetime

def get_backtest_settings(name, tickers, first_date, last_date, initial_amount, currency, needed_depth, rolling, 
                          indicator_name, indicator_building_type, indicator_parameters,
                          quantity_type, allocation):
        
    backtest_settings = {}
    backtest_settings['tickers'] = []
    backtest_settings['quantity_computers'] = []
    backtest_settings['indicator_settings'] = []
    backtest_settings['trading_block_settings'] = []
    backtest_settings['condition_bundle_settings'] = []
    backtest_settings['quantity_settings'] = []
    
    backtest_settings['name'] = name
    backtest_settings['first_date'] = first_date
    backtest_settings['last_date'] = last_date
    backtest_settings['needed_depth'] = needed_depth
    backtest_settings['currency'] = currency
    backtest_settings['rolling'] = rolling
    backtest_settings['amount'] = initial_amount
    
    for ticker in tickers:
        backtest_settings['tickers'].append(ticker)
        backtest_settings['quantity_computers'].append(quantity_type)
        
        indicator_settings = {}
        indicator_settings['ticker'] = ticker
        indicator_settings['indicator_type'] = indicator_name
        indicator_settings['building_type'] = indicator_building_type
        indicator_settings['parameters'] = indicator_parameters
        indicator_settings['name'] = indicator_name
        
        backtest_settings['indicator_settings'].append(indicator_settings)
        
        trading_block_buy_settings = {}
        trading_block_buy_settings['name'] = 'Buy'+ticker
        trading_block_buy_settings['order_type'] = 'BUY'
        trading_block_buy_settings['ticker'] = ticker
        
        backtest_settings['trading_block_settings'].append(trading_block_buy_settings)
        
        trading_block_sell_settings = {}
        trading_block_sell_settings['name'] = 'Sell'+ticker
        trading_block_sell_settings['order_type'] = 'SELL'
        trading_block_sell_settings['ticker'] = ticker
        
        backtest_settings['trading_block_settings'].append(trading_block_sell_settings)
        
        condition_bundle_buy_settings = {}
        condition_bundle_buy_settings['regime_type'] = 'BULL'
        condition_bundle_buy_settings['trading_block_name'] = 'Buy'+ticker
        condition_bundle_buy_settings['indicator_name'] = indicator_name
        
        backtest_settings['condition_bundle_settings'].append(condition_bundle_buy_settings)
        
        condition_bundle_sell_settings = {}
        condition_bundle_sell_settings['regime_type'] = 'BEAR'
        condition_bundle_sell_settings['trading_block_name'] = 'Sell'+ticker
        condition_bundle_sell_settings['indicator_name'] = indicator_name
        
        backtest_settings['condition_bundle_settings'].append(condition_bundle_sell_settings)
        
        quantity_buy_settings = {}
        quantity_buy_settings['allocation'] = allocation
        quantity_buy_settings['quantity_computer_type'] = quantity_type
        quantity_buy_settings['trading_block_name'] = 'Buy'+ticker
        
        backtest_settings['quantity_settings'].append(quantity_buy_settings)
        
        quantity_sell_settings = {}
        quantity_sell_settings['allocation'] = allocation
        quantity_sell_settings['quantity_computer_type'] = quantity_type
        quantity_sell_settings['trading_block_name'] = 'Sell'+ticker
        
        backtest_settings['quantity_settings'].append(quantity_sell_settings)

    return backtest_settings
    
if __name__ == '__main__':
    
    name = 'Strategy'
    tickers = ['AD','EC','SF','JY','BP','CD','MP',
               'HU','CL','HO','NG',
               'ED','TY','US',
               'S','O','W','C','BO','SM',
               'ND','SP',
               'LC','LH','FC',
               'SI','PA','PL','GC','HG',
               'SB','CT','OJ','CC','KC','LB']
    first_date = datetime(2008,1,2)
    last_date = datetime(2012,12,31)
    initial_amount = 1.e6
    currency = 'USD'
    needed_depth = 500
    rolling = 'EOM'
    indicator_name = 'SMA'
    indicator_building_type = 'ONE_LINE_SLOPE'
    indicator_parameters = '150'
    quantity_type = 'RISK_UNITS'
    allocation = 10.
    
    server = xmlrpclib.Server('http://localhost:8080/')
    
    backtest_settings = get_backtest_settings(name, tickers, first_date, last_date, initial_amount, currency, needed_depth, rolling, 
                                                  indicator_name, indicator_building_type, indicator_parameters, 
                                                  quantity_type, allocation)
    
    strategy = server.get_computed_strategy(backtest_settings)
    
    for line in strategy:
        print "%s\t%f"%(line[0],line[1])
            

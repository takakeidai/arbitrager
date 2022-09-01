from binance.um_futures import UMFutures
from utils.timestamp import python_timestamp_to_binance_timestamp,binance_timestamp_to_python_timestamp
from app.models.ticker import Ticker
from app.models.trade import Trade
import settings
import logging

logger = logging.getLogger(__name__)

class DataStructureForBinanceTicker():
    def __init__(self, data):
        self.data = data
    
    @property 
    def past_ticker_price(self):
        return float(self.data[0][4])
    
    @property    
    def past_ticker_volume(self):
        return float(self.data[0][5])
    
    @property
    def realtime_price(self):
        return float(self.data['price'])
    
    @property
    def realtime_timestamp(self):
        return binance_timestamp_to_python_timestamp(self.data['time'])

class DataStructureForBinanceTrade():
    def __init__(self, data):
        self.data = data
        
    @property
    def price(self):
        return self.data['avgPrice']
    
    @property
    def order_status(self):
        if self.data['status'] == 'NEW':
            return True
        else:
            return False
    
    @property
    def units(self):
        return self.data['origQty']

class DataStructureForPosition():
    def __init__(self, data):
        self.data = data
    @property
    def response(self):
        return self.data[0]


class Position():
    def __init__(self, **kwargs):
        self.product_code = kwargs['product_code']
        self.units = kwargs['units']
        self.side = kwargs['side']
        self.mark_price = kwargs['mark_price']


class Binance():
    def __init__(self, **kwargs):
        self.account_key = kwargs['account_key']
        self.api_secret = kwargs['api_secret']
        base_url = kwargs['base_url']
        self.client = UMFutures(key = self.account_key, secret = self.api_secret, base_url = base_url)
        
    
    def get_past_ticker(self, **kwargs):
        # klines -> Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.
        try:
            product_code = kwargs['product_code']
            print(f'Clinet=Binance action=get_past_ticker status=starts {product_code}')
            target_timestamp = python_timestamp_to_binance_timestamp(kwargs['target_timestamp'])
            params = {
                "symbol":product_code,
                "contractType":'PERPETUAL',
                "interval":settings.interval_for_binance,
                "limit":settings.limit,
                "endTime":target_timestamp
            }
            response_data = DataStructureForBinanceTicker(self.client.klines(**params))
            print(f'Clinet=Binance action=get_past_ticker status=ends {product_code}')
            return Ticker(
                product_code = product_code, 
                timestamp = target_timestamp,
                price = response_data.past_ticker_price,
                volume = response_data.past_ticker_volume
                )
            
            
        except Exception as e:
            logger.error(f"Client=Binance action=get_past_ticker error={e}")
            raise
            
    def get_realtime_ticker(self, **kwargs):
        # ticker_price -> Latest price for a symbol or symbols.
        try:
            product_code = kwargs['product_code']
            print(f'Clinet=Binance action=get_realtime_ticker status=starts {product_code}')
            param = {
                "symbol" : product_code,
                }
            response_data = DataStructureForBinanceTicker(self.client.ticker_price(**param))
            print(f'Clinet=Binance action=get_realtime_ticker status=ends {product_code}')
            return Ticker(
                product_code = product_code,
                price = response_data.realtime_price,
                timestamp = response_data.realtime_timestamp
            )
        except Exception as e:
            logger.error(f"Client=Binance action=get_realtime_ticker error={e}")
            raise
        
    def open_trade(self, **kwargs):
        # new_order
        try:
            product_code = kwargs['product_code']
            side_of_binance = kwargs['side_of_binance']
            units = kwargs['units']
            if side_of_binance:
                side = 'BUY'
            else:
                side = 'SELL'
                
            params = {
                'symbol':product_code,
                'side':side,
                'type':'MARKET',
                'quantity':units
            }
            response_data = DataStructureForBinanceTrade(self.client.new_order(**params))
            position = self.get_position(product_code)
            mark_price = position.mark_price
            if response_data.order_status:
                trade = Trade(
                    is_successed = True,
                    product_code = product_code,
                    side = side,
                    price = mark_price,
                    units = response_data.units
                )
            else:
                trade = Trade(
                    is_successed = False,
                    product_code = product_code,
                    side = None,
                    price = None,
                    units = None
                )
            return trade        
        except Exception as e:
            logger.error(f"Client=Binance action=open_trade error={e}")
            raise
    

    
    def get_position(self, product_code):
        try:
            response_data = DataStructureForPosition(self.client.get_position_risk(symbol = product_code))
            if float(response_data.response['positionAmt']) > 0:
                side = 'BUY'
            elif float(response_data.response['positionAmt']) < 0:
                side  = 'SELL'
            else:
                side = None
            
            position = Position(
                product_code = response_data.response['symbol'],
                units = float(response_data.response['positionAmt']),
                side = side,
                mark_price = response_data.response['markPrice']
            )
            return position
        except Exception as e:
            logger.error(f"Client=Binance action=get_position error={e}")
            raise
         
            
    def close_trade(self, **kwargs):
        # new_order
        try:
            product_code = kwargs['product_code']
            position = self.get_position(product_code)
            side = position.side
            if not side:
                trade = Trade(
                    is_successed = False,
                    product_code = product_code,
                    side = None,
                    price = None,
                    units = None
                )  
                return trade
            
            if side == 'BUY':
                side = 'SELL'
            elif side == 'SELL':
                side = 'BUY'     
                
            units = abs(position.units)
            params = {
                'symbol' : product_code,
                'side' : side,
                'type' : 'MARKET',
                'quantity' : units    
            }
            response_data = DataStructureForBinanceTrade(self.client.new_order(**params))
            if response_data.order_status:
                trade = Trade(
                    is_successed = True,
                    product_code = product_code,
                    side = side,
                    price = position.mark_price,
                    units = response_data.units
                )
            else:
                trade = Trade(
                    is_successed = False,
                    product_code = product_code,
                    side = None,
                    price = None,
                    units = None
                )
            return trade
        except Exception as e:
            logger.error(f"Client=Binance action=close_trade error={e}")
            raise
    
# end of line break

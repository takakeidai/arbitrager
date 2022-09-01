from pybit.usdt_perpetual import HTTP
from utils.timestamp import convert_timestamp_to_int
from app.models.ticker import Ticker
from app.models.trade import Trade
import settings
import logging

logger = logging.getLogger(__name__)


class Param():
    def __init__(self, **kwargs):
        pass

class DataStructureForBybitTicker():
    def __init__(self, data):
        self.data = data
        
    @property
    def past_ticker_price(self):
        return float(self.data['result'][0]['close'])

    @property
    def past_ticker_volume(self):
        return float(self.data['result'][0]['volume'])
    
    @property
    def realtime_price(self):
        return float(self.data['result'][0]['price'])
    
    @property
    def realtime_timestamp(self):
        return convert_timestamp_to_int(self.data['time_now'])

class DataStructureForBybitOpen():
    def __init__(self, data):
        self.data = data
    
    @property
    def order_status(self):
        if self.data['result']['order_status'] == 'Created':
            return True
        else:
            return False 
    @property
    def price(self):
        return self.data['result']['price']
    
    @property
    def units(self):
        return self.data['result']['qty']
    
    @property
    def side(self):
        return self.data['side']


'''
[
    {'ret_code': 0, 
    'ret_msg': 'OK', 
    'ext_code': '', 
    'ext_info': '', 
    'result': 
    {'order_id': 'b0185164-520c-4fb5-bec1-88c199c38b1e', 
    'user_id': 608135, 
    'symbol': 'BTCUSDT', 
    'side': 'Sell', 
    'order_type': 'Market', 
    'price': 20505, 
    'qty': 1, 
    'time_in_force': 'ImmediateOrCancel', 
    'order_status': 'Created', 
    'last_exec_price': 0, 
    'cum_exec_qty': 0, 
    'cum_exec_value': 0, 
    'cum_exec_fee': 0,
    'reduce_only': True, 
    'close_on_trigger': True,
    'order_link_id': '', 
    'created_time': '2022-07-09T11:55:07Z', 
    'updated_time': '2022-07-09T11:55:07Z',
    'take_profit': 0, 
    'stop_loss': 0, 
    'tp_trigger_by': 'UNKNOWN', 
    'sl_trigger_by': 'UNKNOWN', 
    'position_idx': 1}, 
    'time_now': '1657367707.205432', 
    'rate_limit_status': 99, 
    'rate_limit_reset_ms': 1657367707203, 
    'rate_limit': 100}
    ]

'''
class DataStructureForBybitClose():
    def __init__(self, data):
        self.data = data[0]['result']
    
    @property
    def price(self):
        return self.data['price']
    @property
    def side(self):
        return self.data['side']
    @property
    def units(self):
        return self.data['qty']
    def order_status(self):
        if self.data['order_status'] == 'Created':
            return True
        else:
            return False 


class DataStructureForPosition():
    def __init__(self, data):
        self.data = data['result']
    @property
    def side(self):
        return self.data['side']
    @property
    def units(self):
        return self.data['size']

class Position():
    def __init__(self, **kwargs):
        self.product_code = kwargs['product_code']
        self.units = kwargs['units']
        self.side = kwargs['side']
  
class Bybit():
    def __init__(self, **kwargs):
        self.account_key = kwargs['account_key']
        self.api_secret = kwargs['api_secret']
        self.bybit_end_point = kwargs['bybit_end_point']
        self.client = HTTP(
            endpoint = self.bybit_end_point,
            api_key = self.account_key,
            api_secret = self.api_secret
        )
    
    def get_past_ticker(self, **kwargs):
        # query_kline -> Get kline
        # return Ticker Object
        try:
            print('Clinet=Bybit action=get_past_ticker status=starts')
            product_code = kwargs['product_code']
            target_timestamp = kwargs['target_timestamp']
            params = {
                "symbol":product_code,
                "interval":settings.interval,
                "limit":settings.limit,
                "from_time":target_timestamp
            }
            response_data = DataStructureForBybitTicker(self.client.query_kline(**params))
            print('Clinet=Bybit action=get_past_ticker status=ends')
            return Ticker(
                product_code = product_code, 
                timestamp = target_timestamp,
                price = response_data.past_ticker_price,
                volume = response_data.past_ticker_volume
            )
        except Exception as e:
            logger.error(f"Client=Bybit action=get_past_ticker error={e}")
            raise
        
    def get_realtime_ticker(self, **kwargs):
        # public_trading_records -> Get recent trades.
        try:
            print('Clinet=Bybit action=get_realtime_ticker status=starts')
            product_code = kwargs['product_code']
            response_data = DataStructureForBybitTicker(self.client.public_trading_records(limit = settings.limit, symbol = product_code))
            print('Clinet=Bybit action=get_realtime_ticker status=ends')
            return Ticker(
                product_code = product_code,
                price = response_data.realtime_price,
                timestamp = response_data.realtime_timestamp
            )
        except Exception as e:
            logger.error(f"Client=Bybit action=get_realtime_ticker error={e}")
            raise
    
    def open_trade(self, **kwargs):
        # place_active_order_bulk
        try:
            product_code = kwargs['product_code']
            side_of_bybit = kwargs['side_of_bybit']
            units = kwargs['units']
            if side_of_bybit:
                side = 'Buy'
            else:
                side = 'Sell'
                
            params = {
                'symbol':product_code,
                'side':side,
                'order_type':'Market',
                'qty':units,
                'reduce_only':False,
                'time_in_force':"GoodTillCancel",
                'close_on_trigger':False
            }
            response_data = DataStructureForBybitOpen(self.client.place_active_order(**params))
            if response_data.order_status:
                trade = Trade(
                    is_successed = True,
                    product_code = product_code,
                    side = side,
                    price = response_data.price,
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
            logger.error(f"Client=Bybit action=open_trade error={e}")
            raise
    
    def get_position(self, product_code):
        try:
            response_data = DataStructureForPosition(self.client.my_position(symbol = product_code))
            position = Position(
                product_code = product_code,
                units = float(response_data.units),
                side = response_data.side
            )
            return position
        except Exception as e:
            logger.error(f"Client=Bybit action=get_position error={e}")
            raise
    
    
    def close_trade(self, **kwargs):
        # close_position
        try:
            product_code = kwargs['product_code']
            response_data = DataStructureForBybitClose(self.client.close_position(product_code))
            if response_data.order_status:
                trade = Trade(
                    is_successed = True,
                    product_code = product_code,
                    side = response_data.side,
                    price = response_data.price,
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
            logger.error(f"Client=Bybit action=close_trade error={e}")
            raise
        
# end of line break

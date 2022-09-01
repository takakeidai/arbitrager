
class Trade():
    def __init__(self, **kwargs):
        self.is_successed = kwargs['is_successed']
        self.side = kwargs['side']
        self.product_code = kwargs['product_code']
        self.units = kwargs['units']
        # self.timestamp = kwargs['timestamp']
        self.price = kwargs['price']

class Trades():
    def __init__(self, **kwargs):
        self.is_successed = kwargs['is_successed']
        self.product_code = kwargs['product_code']
        self.units = kwargs['units']
        self.timestamp = kwargs['timestamp']
        self.bybit_price = kwargs['bybit_price']
        self.side_of_bybit = kwargs['side_of_bybit']
        self.binance_price = kwargs['binance_price']
        self.side_of_binance = kwargs['side_of_binance']
        self.approx_profit = kwargs['approx_profit'] if 'approx_profit' in kwargs.keys() else None
    
# end of line break

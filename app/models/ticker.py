class Ticker():
    def __init__(self,**kwargs):
                self.product_code = kwargs['product_code']
                self.timestamp = kwargs['timestamp']
                self.price = kwargs['price']
                self.volume = kwargs['volume'] if 'volume' in kwargs.keys() else None
                self.open_interest = kwargs['open_interest'] if 'open_interest' in kwargs.keys() else None

        
class Tickers():
    def __init__(self, **kwargs):
        self.product_code = kwargs['product_code']
        self.timestamp = kwargs['timestamp']
        self.bybit_price = kwargs['bybit_price']
        self.binance_price = kwargs['binance_price']
        self.bybit_volume = kwargs['bybit_volume'] if 'bybit_volume' in kwargs.keys() else None
        self.binance_volume = kwargs['binance_volume'] if 'binance_volume' in kwargs.keys() else None
        self.bybit_open_interest = kwargs['bybit_open_interest'] if 'bybit_open_interest' in kwargs.keys() else None
        self.binance_open_interest = kwargs['binance_open_interest'] if 'binance_open_interest' in kwargs.keys() else None
        
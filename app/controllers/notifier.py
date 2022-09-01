import requests
from utils.timestamp import generate_timestamp_for_now, timestamp_to_date, convert_timestamp_to_int

class Notify():
    def __init__(self, **kwargs):
        self.line_token = kwargs['line_token']
        self.line_end_point = kwargs['line_end_point']
        
    def notify_message(self):
        message = f'トレードを開始しました。'
        url = self.line_end_point
        headers = {
            "Authorization":f"Bearer {self.line_token}"
        }
        data = {
            'message':message
        }
        requests.post(
            url,
            headers=headers,
            data = data
        )
        
    def notify_pre_judgement(self, **kwargs):
        product_code = kwargs['product_code']
        timestamp = kwargs['timestamp'] if 'timestamp' in kwargs.keys() else None
        if not timestamp:
            timestamp = timestamp_to_date(convert_timestamp_to_int(generate_timestamp_for_now()))
        url = self.line_end_point
        message = f'\n[{timestamp}]\n[{product_code}]\nの価格の乖離を検知しました。\nエントリー判断を行います。'
        headers = {
            "Authorization":f"Bearer {self.line_token}"
        }
        data = {
            'message':message
        }
        requests.post(
            url,
            headers=headers,
            data = data
        )
    
    def notify_open_trade(self, **kwargs):
        timestamp = kwargs['timestamp']
        product_code = kwargs['product_code']
        bybit_price = kwargs['bybit_price']
        binance_price = kwargs['binance_price']
        url = self.line_end_point
        message = f'\n[{timestamp}]\n[{product_code}]\nBybit=${bybit_price}\nBinance=${binance_price}でエントリーしました。'
        headers =   {
            "Authorization":f"Bearer {self.line_token}"
        }
        data = {
            'message':message
        }
        requests.post(
            url,
            headers=headers,
            data = data
        )

    def notify_close_trade(self, **kwargs):
        timestamp = kwargs['timestamp']
        product_code = kwargs['product_code']
        bybit_price = kwargs['bybit_price']
        binance_price = kwargs['binance_price']
        profit_loss_calculator = kwargs['profit_loss_calculator']
        apporx_profit = profit_loss_calculator.calculate_profit_loss()
        url = self.line_end_point
        message = f'\n[{timestamp}]\n[{product_code}]\nBybit=${bybit_price}\nBinance=${binance_price}でポジションをクローズしました。'
        headers =   {
            "Authorization":f"Bearer {self.line_token}"
        }
        data = {
            'message':message
        }
        requests.post(
            url,
            headers=headers,
            data = data
        )
        
# end of line break

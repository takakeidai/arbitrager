from app.models.ticker import Tickers
from app.models.trade import Trades
from utils.timestamp import generate_timestamp_for_now
import logging

logger = logging.getLogger(__name__)

class ApiManager():
    def __init__(self, **kwargs):
        self.bybit = kwargs['bybit']
        self.binance = kwargs['binance']
        self.units_calculator = kwargs['units_calculator']
        self.multi_thread = kwargs['multi_thread']
        self.judge = kwargs['judge']
            
    def get_past_ticker(self, product_code, target_timestamp, profit_loss_calculator):
        try:
            return_value = self.multi_thread.multi_thread(
                method_1= self.bybit.get_past_ticker, 
                method_2 = self.binance.get_past_ticker, 
                product_code = product_code,
                target_timestamp = target_timestamp
                )
            # ここでmulti_threadで2つのデータをデータベースへ記録
            # return_value.show_value_1(), return_value.show_value_2()をデータベースへ追加。
            past_tickers = Tickers(
                product_code = product_code,
                timestamp = target_timestamp,
                bybit_price = return_value.show_value_1().price,
                binance_price = return_value.show_value_2().price,
                bybit_volume = return_value.show_value_1().volume,
                binance_volume = return_value.show_value_2().volume,
                bybit_open_interest = return_value.show_value_1().open_interest,
                binance_open_interest = return_value.show_value_2().open_interest
                )
            
            return self.judge.determinate_pre_judgement(past_tickers, profit_loss_calculator)
        
        except Exception as e:
            logger.error(f"Client=ApiManager action=get_past_ticker error={e}")
            raise
                
    def get_realtime_ticker_for_open(self, product_code, profit_loss_calculator):
        try:
            return_value = self.multi_thread.multi_thread(
                method_1= self.bybit.get_realtime_ticker, 
                method_2 = self.binance.get_realtime_ticker, 
                product_code = product_code                
                )
            
            realtime_ticker = Tickers(
                product_code = product_code,
                timestamp = None,
                bybit_price = return_value.show_value_1().price,
                binance_price = return_value.show_value_2().price,
                bybit_volume = return_value.show_value_1().volume,
                binance_volume = return_value.show_value_2().volume,
                bybit_open_interest = return_value.show_value_1().open_interest,
                binance_open_interest = return_value.show_value_2().open_interest
            ) 
            
            return self.judge.deteminate_go_nogo(realtime_ticker, profit_loss_calculator)
            
        except Exception as e:
            logger.error(f"Client=ApiManager action=get_realtime_ticker_for_open error={e}")
            raise
    
    def get_realtime_ticker_for_close(self, product_code):
        try:
            return_value = self.multi_thread.multi_thread(
                method_1= self.bybit.get_realtime_ticker, 
                method_2 = self.binance.get_realtime_ticker, 
                product_code = product_code                
                )
            
            realtime_ticker = Tickers(
                product_code = product_code,
                timestamp = None,
                bybit_price = return_value.show_value_1().price,
                binance_price = return_value.show_value_2().price,
                bybit_volume = return_value.show_value_1().volume,
                binance_volume = return_value.show_value_2().volume,
                bybit_open_interest = return_value.show_value_1().open_interest,
                binance_open_interest = return_value.show_value_2().open_interest
            ) 
            
            return self.judge.determinate_close_judgement(realtime_ticker)
            
        except Exception as e:
            logger.error(f"Client=ApiManager action=get_realtime_ticker_for_close error={e}")
            raise
                
    def open_trade(self, **kwargs):
        try:
            product_code = kwargs['product_code']
            side_of_bybit = kwargs['side_of_bybit']
            bybit_price = kwargs['bybit_price']
            side_of_binance = kwargs['side_of_binance']
            binance_price = kwargs['binance_price']
            units = self.units_calculator.get_units(bybit_price = bybit_price, binance_price = binance_price)
            if side_of_bybit == side_of_binance:
                trades = Trades(
                    product_code = product_code,
                    timestamp = generate_timestamp_for_now(),
                    bybit_price = None,
                    side_of_bybit = None,
                    binance_price = None,
                    side_of_binance = None,
                    units = None,
                    is_successed = False                    
                    )
                return trades
            
            return_value = self.multi_thread.multi_thread(
                method_1 = self.bybit.open_trade,
                method_2 = self.binance.open_trade,
                product_code = product_code,
                side_of_bybit = side_of_bybit,
                side_of_binance = side_of_binance,
                units = units
            )
            if return_value.show_value_1().is_successed and return_value.show_value_2().is_successed:
                # trade_units = self.units_calculator.current_units(return_value.show_value_1().units, return_value.show_value_2().units)
                
                trades = Trades(
                    product_code = product_code,
                    timestamp = generate_timestamp_for_now(),
                    bybit_price = return_value.show_value_1().price,
                    side_of_bybit = return_value.show_value_1().side.upper(),
                    binance_price = return_value.show_value_2().price,
                    side_of_binance = return_value.show_value_2().side.upper(),
                    units = return_value.show_value_1().units,
                    is_successed = True     
                )
                # ここでデータベースに書き込む
            else:
                trades = Trades(
                    product_code = product_code,
                    timestamp = generate_timestamp_for_now(),
                    bybit_price = None,
                    side_of_bybit = None,
                    binance_price = None,
                    side_of_binance = None,
                    units = None,
                    is_successed = False                    
                    )
            return trades
        except Exception as e:
            logger.error(f"Client=ApiManager action=open_trade error={e}")
            raise
            
    def close_trade(self, product_code, profit_loss_calculator):
        try:
            return_value = self.multi_thread.multi_thread(
                method_1 = self.bybit.close_trade,
                method_2 = self.binance.close_trade,
                product_code = product_code
            )
            if return_value.show_value_1().is_successed and return_value.show_value_2().is_successed:
                # trade_units = self.units_calculator.current_units(return_value.show_value_1().units, return_value.show_value_2().units)
                trades = Trades(
                    product_code = product_code,
                    timestamp = generate_timestamp_for_now(),
                    bybit_price = return_value.show_value_1().price,
                    side_of_bybit = return_value.show_value_1().side.upper(),
                    binance_price = return_value.show_value_2().price,
                    side_of_binance = return_value.show_value_2().side.upper(),
                    units = return_value.show_value_1().units,
                    is_successed = True,
                    approx_profit = profit_loss_calculator.calculate_profit_loss(
                        return_value.show_value_1().price, 
                        return_value.show_value_2().price
                        )
                )
                # ここでエントリー専用の表にデータを書き込む
            else:
                trades = Trades(
                    product_code = product_code,
                    timestamp = generate_timestamp_for_now(),
                    bybit_price = None,
                    side_of_bybit = None,
                    binance_price = None,
                    side_of_binance = None,
                    units = None,
                    is_successed = False,
                    approx_profit=None
                    )  
            return trades
        except Exception as e:
            logger.error(f"Client=ApiManager action=close_trade error={e}")
            raise
    
if __name__ == '__main__':
    # Do Test in main.py
    # ApiManager
    # from api.api_manager import ApiManager
    # from app.models.multi_thread import MultiThread
    # from app.controllers.judge import Judge
    # from api.binance_api import Binance
    # from api.bybit_api import Bybit
    # from utils.timestamp import generate_timestamp_before_time_delta
    # import settings
    # judge = Judge()
    # multi_thread = MultiThread()
    # binance = Binance(account_key = settings.ak_binance, api_secret = settings.as_binance, base_url = settings.base_url)
    # bybit = Bybit(account_key = settings.ak_bybit, api_secret = settings.as_bybit, bybit_end_point = settings.bybit_end_point)
    # api_manager = ApiManager(bybit = bybit, binance = binance, judge = judge, multi_thread = multi_thread)
    # timestamp = generate_timestamp_before_time_delta()
    # product_code = 'BTCUSDT'

    # #テスト1 get_past_tickerの動作確認
    # judgement = api_manager.get_past_ticker(target_timestamp = timestamp, product_code=product_code)
    # print(judgement.pre_judgement)
    # print(judgement.entry_judgement)
    # print(judgement.side_of_binance)
    # print(judgement.side_of_binance)
    
    #テスト2 : get_realtime_ticker_for_openの動作確認
    # judgement = api_manager.get_realtime_ticker_for_open(product_code)
    # print(judgement.pre_judgement)
    # print(judgement.entry_judgement)
    # print(judgement.side_of_binance)
    # print(judgement.side_of_binance)
    
    # テスト3 : get_realtime_ticker_for_closeの動作確認
    # pass
    
    # テスト4 : open_tradeの動作確認
    # trades = api_manager.open_trade(product_code = product_code, side_of_bybit = True, side_of_binance = False)
    # print(trades.is_successed) 
    # print(trades.product_code) 
    # print(trades.timestamp)
    # print(trades.bybit_price)
    # print(trades.side_of_bybit)
    # print(trades.binance_price)
    # print(trades.side_of_binance)

    # テスト4-2 : open_tradeの動作確認2
    # trades = api_manager.open_trade(product_code = product_code, side_of_bybit = True, side_of_binance = True)
    # print(trades.is_successed) 
    # print(trades.product_code) 
    # print(trades.timestamp)
    # print(trades.bybit_price)
    # print(trades.side_of_bybit)
    # print(trades.binance_price)
    # print(trades.side_of_binance)

    
    # テスト5 : close_tradeの動作確認
    # trades = api_manager.close_trade(product_code = product_code)
    # print(trades.is_successed) 
    # print(trades.product_code) 
    # print(trades.timestamp)
    # print(trades.bybit_price)
    # print(trades.side_of_bybit)
    # print(trades.binance_price)
    # print(trades.side_of_binance)
    pass
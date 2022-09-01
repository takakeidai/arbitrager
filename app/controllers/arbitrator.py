from utils import timestamp
from app.controllers.profit_loss_calculator import ProfitLossCalculator
import time
import logging


logger = logging.getLogger(__name__)

class Arbitrator():
    def __init__(self, **kwargs):
        self.is_trading = False
        self.api_manager = kwargs['api_manager']
        self.units_calculator = kwargs['units_calculator']
        self.product_codes = kwargs['product_codes']
        self.notifier = kwargs['notifier']
        
    def start_arbitrage(self):
        try:
            self.notifier.notify_message()
            self.profit_loss_calculator = ProfitLossCalculator(units_calculator = self.units_calculator)
            self.circulator()
        except Exception as e:
            logger.error(f"Client=Arbitrator action=start_arbitrage error={e}")
            raise        

    # Circulator 
    def circulator(self):
        try:
            for product_code in self.product_codes.product_codes:
                if not self.product_codes.product_codes[product_code]['is_trading']:
                    self.check_market_for_open(self.product_codes.product_codes[product_code]['product_code'])
                else:
                    self.check_market_for_close(self.product_codes.product_codes[product_code]['product_code'])
        except Exception as e:
            logger.error(f"Client=Arbitrator action=circulator error={e}")
            raise
        
        print('Stand-by for 1 min ')
        time.sleep(60)
        print('Ready to go')
        return self.start_arbitrage()
    
    # Open Trade
    def check_market_for_open(self, product_code):
        try:
            target_timestamp = timestamp.generate_timestamp_before_time_delta()
            pre_judgement = self.api_manager.get_past_ticker(product_code, target_timestamp, self.profit_loss_calculator)
            if pre_judgement.pre_judgement:
                #if pre_judgement is True, notiy_pre_judgement
                self.notifier.notify_pre_judgement(product_code = product_code, timestamp = target_timestamp)
                self.check_for_entry(product_code)
            else:
                pass
        except Exception as e:
            logger.error(f"Client=Arbitrator action=check_market_for_open error={e}")
            raise
        
    def check_for_entry(self, product_code):
        entry_judgement =  self.api_manager.get_realtime_ticker_for_open(product_code)
        if entry_judgement.entry_judgement:
            self.open_trade(
                product_code = product_code, 
                side_of_bybit = entry_judgement.side_of_bybit,
                side_of_binance = entry_judgement.side_of_binance,
                bybit_price = entry_judgement.bybit_price,
                binance_price = entry_judgement.binance_price)
    
    def open_trade(self, **kwargs):
        try:
            product_code = kwargs['product_code']
            side_of_bybit = kwargs['side_of_bybit']
            side_of_binance = kwargs['side_of_binance']
            bybit_price = kwargs['bybit_price']
            binance_price = kwargs['binance_price']
            trades = self.api_manager.open_trade(
                product_code = product_code,
                side_of_bybit = side_of_bybit,
                bybit_price = bybit_price,
                side_of_binance = side_of_binance,
                binance_price = binance_price
                )

            if trades.is_successed:
                self.product_codes.product_codes[product_code]['is_trading'] = True
                self.profit_loss_calculator.set_entry_price(
                    entry_bybit_price = trades.bybit_price,
                    entry_binance_price = trades.binance_price
                )
                self.notifier.notify_open_trade(
                    product_code = product_code, 
                    bybit_price = trades.bybit_price, 
                    binance_price = trades.binance_price, 
                    timestamp = trades.timestamp)
            # else:
            #     多くループしている間に価格が変わってしまう可能性があるため、一旦保留。
            #     self.open_trade(product_code, side_of_bybit, side_of_binance)

        except Exception as e:
            logger.error(f"Client=Arbitrator action=open_trade error={e}")
            raise     
        
         
   # Close Trade 

    def check_market_for_close(self, product_code):
        try:
            close_judgement = self.api_manager.get_realtime_ticker_for_close(product_code, self.profit_loss_calculator)
            if close_judgement:
                self.close_trade(product_code, self.profit_loss_calculator)
        except Exception as e:
            logger.error(f"Client=Arbitrator action=check_market_for_close error={e}")
            raise
        
    def close_trade(self, product_code, profit_loss_calculator):
        try:
            trades = self.api_manager.close_trade(product_code, profit_loss_calculator)
            if trades.is_successed:
                self.product_codes.product_codes[product_code]['is_trading'] = False
                self.notifier.notify_close_trade(
                    product_code = product_code, 
                    bybit_price = trades.bybit_price, 
                    binance_price = trades.binance_price, 
                    timestamp = trades.timestamp,
                    profit_loss_calculator = self.profit_loss_calculator
                    )
            else:
                self.close_trade(product_code, profit_loss_calculator)
        except Exception as e:
            logger.error(f"Client=Arbitrator action=close_trade error={e}")
            raise       
    
# end of line break

import settings

class ProfitLossCalculator():
    def __init__(self, **kwargs):
        self.units_calculator = kwargs['units_calculator']
        self.is_profitable = False
        self.entry_bybit_price = None
        self.entry_binance_price = None
        self.bybit_fees = settings.bybit_fees
        self.binance_fees = settings.binance_fees
        
    def set_entry_price(self, **kwargs):
        self.entry_bybit_price = kwargs['entry_bybit_price']
        self.entry_binance_price = kwargs['entry_binance_price']
        
        
    def predict_profit_loss(self, tickers):
        units = self.units_calculator.get_units(
            bybit_price = tickers.bybit_price, 
            binance_price = tickers.binance_price 
            )
        fees_for_bybit = tickers.bybit_price * self.bybit_fees
        fees_for_binance = tickers.binance_price * self.binance_fees
        PL = units * abs(tickers.bybit_price - tickers.binance_price) - fees_for_bybit - fees_for_binance
        if PL >= settings.want_profit:
            self.is_profitable = True
        
        return self.is_profitable
    
    def calculate_profit_loss(self, exit_price_1, exit_price_2):
        pass
    
    def determinate_exit_or_not(self):
        # for trade settlement
        pass
    
    
if __name__ == '__main__':
    pass

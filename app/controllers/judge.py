import settings

class OpenJudgement():
    def __init__(self, **kwargs):
        self.pre_judgement = kwargs['pre_judgement'] if 'pre_judgement' in kwargs.keys() else False
        self.entry_judgement = kwargs['entry_judgement'] if 'entry_judgement' in kwargs.keys() else False
        # when True -> long, False -> short 
        self.side_of_bybit = kwargs['side_of_bybit'] if 'side_of_bybit' in kwargs.keys() else None
        self.side_of_binance = kwargs['side_of_binance'] if 'side_of_binance' in kwargs.keys() else None

class CloseJudgement():
    def __init__(self, **kwargs):
        self.close_judgement = kwargs['close_judgement'] if 'close_judgement' in kwargs.keys() else None

class Judge():
    def __init__(self) -> None:
        pass
    
    def determinate_pre_judgement(self, tickers, profit_loss_calculator):
        if profit_loss_calculator.predict_profit_loss(tickers):
            judgement = OpenJudgement(pre_judgement = True)
        else:
            judgement = OpenJudgement(pre_judgement = False)
        
        return judgement
        
    def deteminate_go_nogo(self, tickers, profit_loss_calculator):
        if profit_loss_calculator.predict_profit_loss(tickers):
            self.determinate_side(tickers)
            
    def determinate_side(self, tickers):
        if tickers.bybit_price > tickers.binance_price:
            judgement = OpenJudgement(entry_judgement = True, side_of_bybit = False, side_of_binance = True)
            return judgement
        
        elif tickers.binance_price > tickers.bybit_price:
            judgement = OpenJudgement(entry_judgement = True, side_of_bybit = True, side_of_binance = False)
            return judgement
        
        judgement = OpenJudgement(entry_judgement = False)
        
        return judgement
    
    def determinate_close_judgement(self, tickers):
        if abs(tickers.bybit_price - tickers.binance_price) <= settings.settlement_epsilon:  
            judgement = CloseJudgement(close_judgement = True)
        else:
            judgement = CloseJudgement(close_judgement = False)
        
        # ここに margin-callのロジックを書く。
        return judgement    
    
# end of line break

        
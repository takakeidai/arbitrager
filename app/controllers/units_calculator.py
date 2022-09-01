import settings

class UnitsCalculator():
    def __init__(self):
        pass
    
    def current_units(self, units_1, units_2):
        if units_1 == units_2:
            return units_1
        return (units_1 + units_2)/2
    
    def mid_price(self, price_1, price_2):
        mid_price = float(price_1 + price_2)/2
        return mid_price
    
    def format_value(self, value):
        return float(format(value, '.3f'))
        
    def get_units(self, **kwargs):
        bybit_price = kwargs['bybit_price']
        binance_price = kwargs['binance_price']
        units = float(settings.funds / self.mid_price(bybit_price, binance_price)) 
        return self.format_value(units)

if __name__ == '__main__':
    pass

    # Do Test in main.py
    # price_1 = 24679.0
    # price_2 = 25649.2
    # uc = UnitsCalculator()
    # print(uc.get_units(bybit_price = price_1, binance_price = price_2))
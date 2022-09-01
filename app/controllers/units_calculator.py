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

# end of line break

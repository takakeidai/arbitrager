
class Order():
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        
    def bybit_order(self):
        self.product_code = self.kwargs['product_code']
        self.side = self.kwargs['side']
        self.order_type = self.kwargs['order_type']
        self.units = self.kwargs['units']
        self.reduce_only = False
        self.time_in_force = "GoodTillCancel"
        self.close_on_trigger = False
        
    def binance_order(self):
        self.product_code = self.kwargs['product_code']
        self.side = self.kwargs['side']        
        self.type = 'MARKET'
        self.quantity = self.kwargs['quantity']

# end of line break

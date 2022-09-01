
'''
codes = {
    'btcusdt':'BTCUSDT', 
    'ethusdt':'ETHUSDT', 
    'bnbusdt':'BNBUSDT'}

{
    'btcusdt': {'product_code':"BTCUSDT", 'is_trading': False},
    'ethusdt': {'product_code':"ETHUSDT", 'is_trading': False},
    'bnbusdt': {'product_code':"BNBUSDT", 'is_trading': False}
    
}

'''

class ProductCodes():
    def __init__(self, codes):
        self.codes = codes
        self.product_codes = {}
        self.create_code_list()
        
    def create_code_list(self):
        for code in self.codes:
            name = code.lower()
            code_dict = dict(product_code = code.upper(), is_trading = False)
            self.product_codes[name] = code_dict
    
    def set_product_code(self, new_code):
        if 'usdt' or 'USDT' not in new_code:
            new_code = new_code + 'usdt'
        name = new_code.lower()
        upper_text = new_code.upper()
        code_dict = dict(product_code = upper_text, is_trading = False)
        self.product_codes[name] = code_dict
    
    def get_product_code(self, code):
        code = code.lower()
        if code not in self.product_codes.keys():
            return None
        return self.product_codes[code]
        
# end of line break

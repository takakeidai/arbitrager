
from dotenv import dotenv_values
from app.controllers.arbitrator import Arbitrator
from api.api_manager import ApiManager
from app.models.product_codes import ProductCodes
from app.models.multi_thread import MultiThread
from app.controllers.judge import Judge
from app.controllers.notifier import Notify
from app.controllers.units_calculator import UnitsCalculator
from app.controllers.profit_loss_calculator import ProfitLossCalculator
from api.binance_api import Binance
from api.bybit_api import Bybit


config = dotenv_values(".env") 
codes = {
    'btcusdt':'BTCUSDT', 
    'ethusdt':'ETHUSDT'}

product_codes = ProductCodes(codes)
units_calculator = UnitsCalculator()
pl_calculator = ProfitLossCalculator(units_calculator = units_calculator)
judge = Judge()
multi_thread = MultiThread()
binance = Binance(account_key = config['AK_BINANCE'], api_secret = config['AS_BINANCE'], base_url = config['BASE_URL'])
bybit = Bybit(account_key = config['AK_BYBIT'], api_secret = config['AS_BYBIT'], bybit_end_point = config['BYBIT_END_POINT']) 
notifier = Notify(line_token = config['LINE_TOKEN'], line_end_point = config['LINE_END_POINT'])
api_manager = ApiManager(bybit = bybit, binance = binance, judge = judge, multi_thread = multi_thread, units_calculator = units_calculator)
arbitrator = Arbitrator(product_codes = product_codes, api_manager = api_manager,  notifier = notifier, units_calculator = units_calculator)
arbitrator.start_arbitrage()

# end of line break

    

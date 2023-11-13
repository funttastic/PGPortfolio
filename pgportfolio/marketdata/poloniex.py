import json
import time
import sys
from datetime import datetime

if sys.version_info[0] == 3:
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import Request, urlopen
    from urllib import urlencode

minute = 60
hour = minute * 60
day = hour * 24
week = day * 7
month = day * 30
year = day * 365

# Novos Endpoints da API
PUBLIC_COMMANDS = {
    'returnTicker': 'markets/ticker24h',
    'return24hVolume': 'markets/ticker24h',
    'returnOrderBook': 'markets/{symbol}/orderBook',
    'returnTradeHistory': 'markets/{symbol}/trades',
    'returnChartData': 'markets/{symbol}/candles',
    'returnCurrencies': 'currencies',
    'returnLoanOrders': 'loanOrders'
}

class Poloniex:
    def __init__(self, APIKey='', Secret=''):
        self.APIKey = APIKey.encode()
        self.Secret = Secret.encode()
        self.timestamp_str = lambda timestamp=time.time(), format="%Y-%m-%d %H:%M:%S": datetime.fromtimestamp(timestamp).strftime(format)
        self.str_timestamp = lambda datestr=self.timestamp_str(), format="%Y-%m-%d %H:%M:%S": int(time.mktime(time.strptime(datestr, format)))
        self.float_roundPercent = lambda floatN, decimalP=2: str(round(float(floatN) * 100, decimalP)) + "%"

    def api(self, command, args={}):
      base_url = 'https://api.poloniex.com/'
      if command in PUBLIC_COMMANDS:
          url = base_url + PUBLIC_COMMANDS[command]
          if '{symbol}' in url:
              url = url.format(symbol=args.get('currencyPair'))

          headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
          print(url + '?' + urlencode(args))
          req = Request(url + '?' + urlencode(args), headers=headers)

          ret = urlopen(req)
          return json.loads(ret.read().decode(encoding='UTF-8'))
      else:
          return False

    def marketTicker(self, x=0):
        return self.api('returnTicker')

    def marketVolume(self, x=0):
        return self.api('return24hVolume')

    def marketStatus(self, x=0):
        return self.api('returnCurrencies')

    def marketLoans(self, coin):
        return self.api('returnLoanOrders',{'currency':coin})

    def marketOrders(self, pair='all', depth=10):
        return self.api('returnOrderBook', {'currencyPair':pair, 'depth':depth})

    def marketChart(self, pair, period=day, start=time.time()-(week*1), end=time.time()):
        return self.api('returnChartData', {'currencyPair':pair, 'period':period, 'start':start, 'end':end})

    def marketTradeHist(self, pair):
        return self.api('returnTradeHistory',{'currencyPair':pair})

# Exemplo de uso
# poloniex = Poloniex()
# print(poloniex.marketTicker())

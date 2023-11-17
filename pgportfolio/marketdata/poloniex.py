import enum

from pgportfolio.constants import FIVE_MINUTES, FIFTEEN_MINUTES, HALF_HOUR, HOUR, TWO_HOUR, FOUR_HOUR, DAY, YEAR
from polosdk import RestClient

class Interval(enum.Enum):
    MINUTE_1="MINUTE_1"
    MINUTE_5="MINUTE_5"
    MINUTE_10="MINUTE_10"
    MINUTE_15="MINUTE_15"
    MINUTE_30="MINUTE_30"
    HOUR_1="HOUR_1"
    HOUR_2="HOUR_2"
    HOUR_4="HOUR_4"
    HOUR_6="HOUR_6"
    HOUR_12="HOUR_12"
    DAY_1="DAY_1"
    DAY_3="DAY_3"
    WEEK_1="WEEK_1"
    MONTH_1="MONTH_1"

    @staticmethod
    def convert(input: int):
        if input == FIVE_MINUTES:
            return Interval.MINUTE_5
        if input == FIFTEEN_MINUTES:
            return Interval.MINUTE_15
        if input == HALF_HOUR:
            return Interval.MINUTE_30
        if input == HOUR:
            return Interval.HOUR_1
        if input == TWO_HOUR:
            return Interval.HOUR_2
        if input == FOUR_HOUR:
            return Interval.HOUR_4
        if input == DAY:
            return Interval.DAY_1
        if input == YEAR:
            raise ValueError(f"Invalid input {input} cannot be converted.")

class Poloniex:
    def __init__(self, APIKey='', Secret=''):
        self.client = RestClient()

    # def marketTicker(self, symbol='BTC_USDT'):
    #     return self.client.markets().get_ticker24h(symbol)

    def marketVolume(self):
        return self.client.markets().get_ticker24h_all()

    def marketStatus(self):
        return self.client.get_currencies(multichain=True)

    # def marketOrders(self, symbol='BTC_USDT'):
    #     return self.client.markets().get_orderbook(symbol)

    def marketChart(self, symbol='BTC_USDT', period=None, start=None, end=None):
        interval = Interval.convert(period).value

        # return self.client.markets().get_candles(symbol, interval, start, end)
        return self.client.markets().get_candles(symbol, interval, start)

    # def marketTradeHist(self, symbol):
    #     return self.client.markets().get_trades(symbol)


if __name__ == "__main__":
    poloniex = Poloniex()
    # print(poloniex.marketTicker())
    # print(poloniex.marketVolume())
    # print(poloniex.marketStatus())
    # print(poloniex.marketOrders())
    print(poloniex.marketChart(period=DAY))
    # print(poloniex.marketTradeHist())

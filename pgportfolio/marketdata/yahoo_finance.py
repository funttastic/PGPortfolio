import enum
import sqlite3
from datetime import datetime, timedelta

import requests
import yfinance as yf


yahoo_finance_pairs = [
	"BTC-USD",
	"LTC-USD",
	"XRP-USD",
	"PPC-USD",
	"USDT-USD",
	"DOGE-USD",
	"XPM-USD",
	"NMC-USD",
	"NVC-USD",
	"VTC-USD",
	"BLK-USD",
	"TRMB-USD",
	"DASH-USD",
	"ZCC-USD",
	"BTS-USD",
	"YBC-USD",
	"NXT-USD",
	"START-USD",
	"MEC-USD",
	"XLM-USD",
	"USNBT-USD",
	"BILS-USD",
	"WDC-USD",
	"BOST-USD",
	"QRK-USD",
	"FTC-USD",
	"MAID-USD",
	"APC-USD",
	"IFC-USD",
	"XMR-USD",
	"TIPS-USD",
	"GRM-USD",
	"DGC-USD",
	"CLAM-USD",
	"ANC-USD",
	"BUCKS-USD",
	"SRC-USD",
	"BLOCK-USD",
	"RIC-USD",
	"VRC-USD",
	"VASH-USD",
	"UNC-USD",
	"XPY-USD",
	"BYC-USD",
	"SDC-USD",
	"TAG-USD",
	"ZET-USD",
	"XDN-USD",
	"CANN-USD",
	"MONA-USD",
	"BCN-USD",
	"BANX-USD",
	"MAX-USD",
	"XEM-USD",
	"ETC-USD",
	"EAC-USD",
	"MINT-USD",
	"XVC-USD",
	"BITUSD-USD",
	"UNITY-USD",
	"BTCD-USD",
	"HYPER-USD",
	"POT-USD",
	"ARCH-USD",
	"MOON-USD",
	"NOTE-USD",
	"IOC-USD",
	"BURST-USD",
	"NET-USD",
	"OMC-USD",
	"SNRG-USD",
	"RDD-USD",
	"XTC-USD",
	"XCP-USD",
	"NKT-USD",
	"MMC-USD",
	"CLOAK-USD",
	"TRON-USD",
	"NSR-USD",
	"FST-USD",
	"NLG-USD",
	"URO-USD",
	"XBS-USD",
	"PANGEA-USD",
	"COL-USD",
	"DTC-USD",
	"BLITZ-USD",
	"HYP-USD",
	"NAS-USD",
	"KARMA-USD",
	"XAUR-USD",
	"BITBTC-USD",
	"UNB-USD",
	"BTB-USD",
	"TIX-USD",
	"DGB-USD",
	"DIBS-USD",
	"COVAL-USD",
	"DMD-USD",
	"XST-USD",
]


class YahooFinanceInterval(enum.Enum):
	ONE_MINUTE = "1m"
	TWO_MINUTES = "2m"
	FIVE_MINUTES = "5m"
	FIFTEEN_MINUTES = "15m"
	THIRTY_MINUTES = "30m"
	SIXTY_MINUTES = "60m"
	NINETY_MINUTES = "90m"
	ONE_HOUR = "1h"
	ONE_DAY = "1d"
	FIVE_DAYS = "5d"
	ONE_WEEK = "1wk"
	ONE_MONTH = "1mo"
	THREE_MONTHS = "3mo"


def get_previous_day(target):
	start_date = datetime.strptime(target, '%Y-%m-%d')
	day_before_start = start_date - timedelta(days=1)

	return day_before_start


def get_top_volume_coins_with_yahoo_finance(start, end, number_of_tokens):
	# Lista pré-definida de criptomoedas (esta lista pode ser expandida ou modificada)
	crypto_symbols = yahoo_finance_pairs

	# Baixa dados de todos os símbolos de uma vez
	data = yf.download(crypto_symbols, start=start, end=end, interval='1d', group_by='ticker')

	volumes = {}
	for symbol in crypto_symbols:
		symbol_data = data[symbol]  # Acessa os dados específicos de cada criptomoeda
		total_volume = symbol_data['Volume'].sum()
		if total_volume > 0:
			volumes[symbol] = total_volume

	# Ordena as criptomoedas pelo volume e pega as 'number_of_tokens' principais
	top_coins = sorted(volumes, key=volumes.get, reverse=True)[:number_of_tokens]
	return top_coins


def get_top_volume_coins_with_coin_market_cap(api_key, start, number_of_tokens):
	url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/historical"
	headers = {
		'Accepts': 'application/json',
		'X-CMC_PRO_API_KEY': api_key,
	}
	parameters = {
		'date': start.strftime('%Y-%m-%d'),  # Formato de data como 'YYYY-MM-DD'
		'limit': 5000  # Número máximo de criptomoedas a serem retornadas
	}

	response = requests.get(url, headers=headers, params=parameters)
	data = response.json()

	# Extrair os dados de volume e ordenar
	volumes = {d['symbol']: d['quote']['USD']['volume_24h'] for d in data['data']}
	top_coins = sorted(volumes, key=volumes.get, reverse=True)[:number_of_tokens]

	return top_coins


def get_top_volume_coins_with_coin_gecko(start, number_of_tokens):
	url = "https://api.coingecko.com/api/v3/coins/markets"
	parameters = {
		'vs_currency': 'usd',
		'order': 'volume_desc',  # Ordenar por volume em ordem decrescente
		'per_page': 250,  # Número de resultados por página
		'page': 1,  # Página de resultados
		'price_change_percentage': '24h',  # Percentual de mudança de preço nas últimas 24 horas
		'sparkline': False,  # Sem gráficos sparkline
		'date': start.strftime('%d-%m-%Y')  # Formato de data como 'DD-MM-YYYY'
	}

	response = requests.get(url, params=parameters)
	data = response.json()

	# Filtrar e obter os símbolos das top 'number_of_tokens' criptomoedas por volume
	top_coins = [coin['symbol'].upper() for coin in data[:number_of_tokens]]

	return top_coins


def get_ohlcv_data(coins, start, end, interval):
	# Baixa dados de todos os símbolos de uma vez
	data = yf.download(coins, start=start, end=end, interval=interval, group_by='ticker')
	
	ohlcv_data = {}
	for coin in coins:
		symbol_data = data[coin]  # Acessa os dados específicos de cada criptomoeda
		ohlcv_data[coin] = symbol_data
	return ohlcv_data


def insert_into_db(data):
	conn = sqlite3.connect('crypto_data.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS History (
					date INTEGER, coin varchar(20), high FLOAT, low FLOAT, 
					open FLOAT, close FLOAT, volume FLOAT, quoteVolume FLOAT, 
					weightedAverage FLOAT, PRIMARY KEY (date, coin));''')

	for coin, df in data.items():
		for index, row in df.iterrows():
			c.execute("INSERT INTO History VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
					  (index.timestamp(), coin, row['High'], row['Low'],
					   row['Open'], row['Close'], row['Volume'], None, None))

	conn.commit()
	conn.close()


if __name__ == '__main__':
	# # Exemplo de uso:
	# start = '2015-07-01'
	# end = '2017-08-01'
	# number_of_tokens = 10
	# interval = '1d' # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
	# top_coins = get_top_volume_coins_with_yahoo_finance(start, end, number_of_tokens)
	# ohlcv_data = get_ohlcv_data(top_coins, start, end, interval)
	# insert_into_db(ohlcv_data)

	# # Uso da função:
	# start = '2015-06-30'
	# number_of_tokens = 10
	# top_coins = get_top_volume_coins_with_yahoo_finance(api_key, start, number_of_tokens)

	# https://coinmarketcap.com/historical/20150701/
	# # Uso da função:
	# api_key = 'SUA_CHAVE_API'
	# start = pd.to_datetime('2015-06-30')
	# number_of_tokens = 10
	# top_coins = get_top_volume_coins_with_coin_market_cap(api_key, start, number_of_tokens)

	# # Uso da função:
	# start = pd.to_datetime('2015-06-30')
	# number_of_tokens = 10
	# top_coins = get_top_volume_coins_with_coin_gecko(start, number_of_tokens)
	# print(top_coins)

	# Exemplo de uso:
	# volume_start = '2015-06-01'
	# volume_end = '2015-06-30'
	# start = '2015-07-01'
	# end = '2017-07-02'
	volume_start = '2017-11-10'
	volume_end = '2017-12-09'
	start = '2017-12-10'
	end = '2023-11-10'
	number_of_tokens = 11
	interval = '1d'
	top_coins = get_top_volume_coins_with_yahoo_finance(volume_start, volume_end, number_of_tokens)
	ohlcv_data = get_ohlcv_data(top_coins, start, end, interval)
	insert_into_db(ohlcv_data)

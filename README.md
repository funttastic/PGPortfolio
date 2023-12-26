Important fork with fixes:
https://github.com/mridulrb/PGPortfolio



mkdir database
cp pgportfolio/marketdata/Data.db.example database/Data.db

python main.py --mode=generate --repeat=1
python main.py --mode=train --processes=1 --device=gpu
python main.py --mode=backtest --algo=1
python main.py --mode=plot --algos=crp,olmar,1 --labels=crp,olmar,nnagent
python main.py --mode=table --algos=1,olmar,ons --labels=nntrader,olmar,ons

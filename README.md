Important fork with fixes:
https://github.com/mridulrb/PGPortfolio



mkdir database
cp pgportfolio/marketdata/Data.db.example database/Data.db

python main.py --mode=generate --repeat=1
python main.py --mode=train --processes=1 --device=gpu
python main.py --mode=backtest --algo=1
python main.py --mode=plot --algos=1,crp,ons,olmar,up,anticor,pamr,best,bk,bcrp,corn,m0,rmr,cwmr,eg,sp,ubah,wmamr --labels=nnagent,crp,ons,olmar,up,anticor,pamr,best,bk,bcrp,corn,m0,rmr,cwmr,eg,sp,ubah,wmamr
python main.py --mode=table --algos=1,crp,ons,olmar,up,anticor,pamr,best,bk,bcrp,corn,m0,rmr,cwmr,eg,sp,ubah,wmamr --labels=nnagent,crp,ons,olmar,up,anticor,pamr,best,bk,bcrp,corn,m0,rmr,cwmr,eg,sp,ubah,wmamr

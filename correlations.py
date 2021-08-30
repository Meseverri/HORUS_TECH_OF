from datetime import datetime
import numpy as np
from numpy.core.numeric import NaN
from numpy.core.records import array
import pytz
import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
market_lists=["AUDCHF","AUDJPY","AUDUSD","CADJPY","EURAUD","EURCAD","EURGBP","USDJPY","EURJPY","EURUSD","GBPCAD","GBPAUD","GBPCHF","GBPJPY","GBPUSD","USDCAD","USDCHF"]

# mostramos los datos sobre el paquete MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# importamos el módulo pandas para mostrar los datos obtenidos en forma de recuadro

pd.set_option('display.max_columns', 500) # cuántas columnas mostramos
pd.set_option('display.width', 1500)      # anchura máx. del recuadro para la muestra
# importamos el módulo pytz para trabajar con el huso horario TC, para que no se aplique el desplazamiento del huso horario local
utc_from = datetime.today()
 
# establecemos la conexión con el terminal MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# establecemos el huso horario en UTC
timezone = pytz.timezone("Etc/UTC")
# creamos el objeto datetime en el huso horario U020 en el huso horario UTC
eurusd = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H1, utc_from, 10000)
markets_open=pd.DataFrame()
for market in market_lists:
    rates= mt5.copy_rates_from(market, mt5.TIMEFRAME_H1, utc_from, 10000)
    rates_pd=pd.DataFrame(rates)
    markets_open[market]=rates_pd["open"]


mt5.shutdown()

print(markets_open.corr().shape)
print(markets_open.corr())
print(markets_open.corr().loc[:,"CADJPY"])
figure = plt.figure()
axes = figure.add_subplot(111)
  
# using the matshow() function 
caxes = axes.matshow(markets_open.corr())
figure.colorbar(caxes)
  
axes.set_xticklabels(['']+markets_open.corr().columns)
axes.set_yticklabels(['']+markets_open.corr().columns)


plt.show()
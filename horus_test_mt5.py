# Copyright 2021, MetaQuotes Ltd.
# https://www.mql5.com

from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
 
# conectamos con MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
 
# solicitamos el estado y los parámetros de conexión
print(mt5.terminal_info())
# obtenemos la información sobre la versión de MetaTrader 5
print(mt5.version())
 
# solicitamos 1000 ticks de EURAUD
euraud_ticks = mt5.copy_ticks_from("EURAUD", datetime(2020,1,28,13), 1000, mt5.COPY_TICKS_ALL)
# solicitamos los ticks de AUDUSD en el intervalo 2019.04.01 13:00 - 2019.04.02 13:00
audusd_ticks = mt5.copy_ticks_range("AUDUSD", datetime(2020,1,27,13), 1000, mt5.COPY_TICKS_ALL)
 
# obtenemos con distintos métodos las barras de diferentes instrumentos
eurusd_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, datetime.today(), 1000)
eurgbp_rates = mt5.copy_rates_from("EURGBP", mt5.TIMEFRAME_M1, datetime.today(), 1000)
eurcad_rates = mt5.copy_rates_range("EURCAD", mt5.TIMEFRAME_M1, datetime(2020,1,27,13), datetime(2020,1,28,13))
print("LAST ERROR----->",mt5.last_error())
# finalizamos la conexión con MetaTrader 5
mt5.shutdown()
print("LAST ERROR----->",mt5.last_error())
#DATA
print('euraud_ticks(', len(euraud_ticks), ')')
for val in euraud_ticks[:10]: print(val)
 
print('audusd_ticks(', len(audusd_ticks), ')')
for val in audusd_ticks[:10]: print(val)
 
print('eurusd_rates(', len(eurusd_rates), ')')
for val in eurusd_rates[:10]: print(val)
 
print('eurgbp_rates(', len(eurgbp_rates), ')')
for val in eurgbp_rates[:10]: print(val)
 
print('eurcad_rates(', len(eurcad_rates), ')')
for val in eurcad_rates[:10]: print(val)
 
#PLOT
# creamos un DataFrame de los datos obtenidos
ticks_frame = pd.DataFrame(euraud_ticks)
ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
print(ticks_frame.head(5))
# dibujamos los ticks en el gráfico
plt.plot(ticks_frame['time'], ticks_frame['ask'], 'r-', label='ask')
plt.plot(ticks_frame['time'], ticks_frame['bid'], 'b-', label='bid')
 
# mostramos los rótulos
plt.legend(loc='upper left')

# añadimos los encabezados
plt.title('EURAUD ticks')
 
# mostramos el gráfico
plt.show()
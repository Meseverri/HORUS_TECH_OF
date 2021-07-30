from datetime import datetime
import numpy as np
import pytz
import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# mostramos los datos sobre el paquete MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# importamos el módulo pandas para mostrar los datos obtenidos en forma de recuadro

pd.set_option('display.max_columns', 500) # cuántas columnas mostramos
pd.set_option('display.width', 1500)      # anchura máx. del recuadro para la muestra
# importamos el módulo pytz para trabajar con el huso horario

 
# establecemos la conexión con el terminal MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# establecemos el huso horario en UTC
timezone = pytz.timezone("Etc/UTC")
# creamos el objeto datetime en el huso horario UTC, para que no se aplique el desplazamiento del huso horario local
utc_from = datetime.today()
# obtenemos 10 barras de EURUSD H4 a partir del 01.10.2020 en el huso horario UTC
rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H1, utc_from, 1000)
 
# finalizamos la conexión con el terminal MetaTrader 5
mt5.shutdown()
# mostramos cada elemento de los datos obtenidos en una nueva línea
print("Mostramos los datos obtenidos como son")
for rate in rates:
    print(rate)
 
# creamos un DataFrame de los datos obtenidos
rates_frame = pd.DataFrame(rates)
# convertimos la hora en segundos al formato datetime
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
rates_frame['variacion log open']=np.log(rates_frame['open'].shift(1) /rates_frame['open'])

# mostramos los datos
print("\nMostramos el frame de datos con la información")
print(rates_frame)  
print(rates_frame['variacion log open'].std())
plt.plot(rates_frame["open"],rates_frame["variacion log open"], 'r.', label="variacion log open")

 
# mostramos los rótulos
plt.legend(loc='upper left')
 
# añadimos los encabezados
plt.title('EURUSD')
 
# mostramos el gráfico
plt.show()
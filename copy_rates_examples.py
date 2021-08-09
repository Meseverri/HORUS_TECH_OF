
# obtenemos 10 barras de EURUSD H4 a partir del 01.10.2
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
# importamos el módulo pytz para trabajar con el huso horario TC, para que no se aplique el desplazamiento del huso horario local
utc_from = datetime.today()
 
# establecemos la conexión con el terminal MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# establecemos el huso horario en UTC
timezone = pytz.timezone("Etc/UTC")
# creamos el objeto datetime en el huso horario U020 en el huso horario UTC
rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H1, utc_from, 10000)
 
# finalizamos la conexión con el terminal MetaTrader 5
mt5.shutdown()

def is_bull(variation):

    if variation<0:
        return False

    elif variation==0: 
        return None

    return True

# mostramos cada elemento de los datos obtenidos en una nueva línea




print("Mostramos los datos obtenidos como son")
for rate in rates[:10]:
    print(rate)
 
# creamos un DataFrame de los datos obtenidos
rates_frame = pd.DataFrame(rates)
# convertimos la hora en segundos al formato datetime

rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
rates_frame.set_index("time")
rates_frame['variacion log open']=np.log(rates_frame['open'].shift(1) /rates_frame['open'])
##rates_frame['is bull']=is_bull(rates_frame['variacion log open'])
bull=[]
for i in rates_frame['variacion log open']:
    bull.append(is_bull(i))

rates_frame['is bull']=bull



pos_log=rates_frame[rates_frame['variacion log open']>=0]
neg_log=rates_frame[rates_frame['variacion log open']<=0]
# mostramos los datos
print("\nMostramos el frame de datos con la información")

print(rates_frame)  
print("\n Crecimientos \n",pos_log)
print("\n Decrecimientos \n",neg_log)
print(rates_frame['variacion log open'].std())
print(rates_frame[rates_frame['variacion log open']>0.006])
print(rates_frame[rates_frame['variacion log open']<-0.006 ])
print(neg_log.index)
print(type(neg_log.index))
fig,axs=plt.subplots(2,3)
axs[0,0].plot(rates_frame["open"],rates_frame["variacion log open"],"r.", label="variacion log open")
axs[0,0].legend(loc='upper left')
axs[0,0].set_title('EURUSD')

axs[0,1].plot(rates_frame["time"],rates_frame["open"],"r--", label="Open")
axs[0,1].legend(loc='upper left')
axs[0,1].set_title('EURUSD')

axs[0,2].hist(rates_frame["variacion log open"],bins=100, label="variacion log open")
axs[0,2].legend(loc='upper left')
axs[0,2].set_title('EURUSD')

axs[1,0].plot(pos_log["open"],pos_log["variacion log open"],"b.",label="variacion log positiva open")
axs[1,0].legend(loc='upper left')
axs[1,0].set_title('EURUSD')

axs[1,1].plot(neg_log["open"],neg_log["variacion log open"],"b.",label="variacion log negativa open")
axs[1,1].legend(loc='upper left')
axs[1,1].set_title('EURUSD')

axs[1,2].plot(rates_frame["tick_volume"],rates_frame["variacion log open"],"g.",label="tick volume")


plt.legend(loc='upper left')
 
# añadimos los encabezado
plt.title('EURUSD')
 
# mostramos el gráfico
plt.show()


 

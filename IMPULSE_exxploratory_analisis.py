# obtenemos 10 barras de EURUSD H4 a partir del 01.10.2
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


# creamos un DataFrame de los datos obtenidos
rates_frame = pd.DataFrame(rates)
# convertimos la hora en segundos al formato datetime

rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
#rates_frame.set_index("time")
rates_frame['variacion log open']=np.log(rates_frame['open'] /rates_frame['open'].shift(1))

# 

bull=[]
for i in rates_frame['variacion log open']:
    bull.append(is_bull(i))

rates_frame['is bull']=bull

#Recibe un data frame de velas con las siguientes columnas:
    # - is bull
    # - time
    # - variacion logaritmica

def momentum_df (df, colum= 'variacion log open'): 
    ret = []
    count = 1 
    sum_acumulada = 0
    fecha_ini = df.iloc[1,0]

    for i, data in enumerate(df.iloc):
        if i > 1:    
            prev_data = df.iloc[i-1]
            if is_bull(data[colum]) is is_bull(prev_data[colum]):
                count+=1
                sum_acumulada += data[colum]
            else:

                ret.append([fecha_ini, prev_data["time"], count, sum_acumulada])

                #despues de depositar en ret
                fecha_ini = data["time"]
                count = 1 
                sum_acumulada = data[colum]

    return pd.DataFrame(ret, columns=["t0","tf","candels","suma acumulada"])


def distribution_df(data,parts=100):
    data=data.round(6)
    minimo=data.min()
    maximo=data.max()
    rango=maximo-minimo
    interval_size=rango/parts
    Index=[]
    dist_data=[]
    
    for k in range(parts+1):    
        Index.append(minimo+k*interval_size)

    print("minimo:",minimo)
    print("maximo:",maximo)
    print(f"{Index[0]},{Index[-1]}")
    for i in Index:  
        count=1
        a=set(data[i<=data]).intersection(set(data[data<(i+count*interval_size)]))
        a=list(a)
        dist_data.append(len(a))
        
        count+=1
    
    dist=pd.DataFrame(dist_data,index=Index)
    return dist

EUROUSD_impulse=momentum_df(rates_frame)
EUROUSD_impulse.set_index("t0")

EUROUSD_pos_impulse=EUROUSD_impulse[EUROUSD_impulse["suma acumulada"]>0]
EUROUSD_neg_impulse=EUROUSD_impulse[EUROUSD_impulse["suma acumulada"]<0]
#distribution_df() 
print(EUROUSD_impulse)

print(rates_frame.iloc[-1])
print(type(EUROUSD_impulse["suma acumulada"]))

x=np.array(EUROUSD_impulse["suma acumulada"].values)
y=EUROUSD_impulse["suma acumulada"]
print("concordancia de tamaños",len(x)==len(y))
print(x)
print(type(y))

fig,axs=plt.subplots(1,2)
axs[0,0].plot(EUROUSD_impulse["suma acumulada"],label="impulses")
axs[0,0].set_title('EURUSD impulse')

axs[0,1].plot(EUROUSD_impulse["candels"],"r.",label="candels")
axs[0,1].set_title('EURUSD candels')
plt.hist2d(EUROUSD_impulse["suma acumulada"],EUROUSD_impulse["candels"],bins=10)
plt.show()

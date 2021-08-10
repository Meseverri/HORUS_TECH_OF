
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
rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H1, utc_from, 1000)
 
# finalizamos la conexión con el terminal MetaTrader 5
mt5.shutdown()
#defino una funcion que a partir de los datos me genere una tabla de frecuencias
#se calcula el rango de datos, [minimo,maximo] en donde existan datos.
#el rango es el max-min
#decidomos las particiones la cual dividiremos el rango de datos

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
#funcion de impulsos, definimos impulso primeramente como el numero de veces seguidas de las variaciones tanto positivas como negativas 
def impulse(series):
    acumulado=0
     
    pass

def is_bull(variation):
    if variation>0:
        return True

    elif variation<0:
        return False
    else: 
        return None




    
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
rates_frame.set_index("time")
rates_frame['variacion log open']=np.log(rates_frame['open'].shift(1) /rates_frame['open'])
bull=[]
for i in rates_frame['variacion log open']:
    bull.append(is_bull(i))

rates_frame['is bull']=bull
Distribution=distribution_df(rates_frame['variacion log open'])
#print(Distribution)
print(len(Distribution))
print(Distribution.head())
plt.plot(Distribution)
plt.show()


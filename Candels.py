"""
Created on Tue Mar  2 09:52:38 2021

@author: mesev
"""
import pandas as pd
import time
from matplotlib import pyplot as plt

def mean(lista):
    n=len(lista)
    acumulado=0
    for i in lista:
        acumulado+=i
    return acumulado/n

def picos(lista):
    P=[]
    count=1
    for i in lista[1:-1]:
        if i>lista[count-1] and i>lista[count+1]:
            P.append([i,count])
        count+=1
    return P
            
def valles(lista):
    P=[]
    count=1
    for i in lista[1:-1]:
        if i<lista[count-1] and i<lista[count+1]:
            P.append([i,count])
        count+=1
    return P




class Candel:
    def __init__(self,ticker,date,time,Open,high,low,close):
        self.ticker=ticker
        self.date=date
        self.time=int(time)
        self.open=float(Open)
        self.high=float(high)
        self.low=float(low)
        self.close=float(close)
        self.bullish=self.isBullish()
        self.size=self.candelSize()
        
    def isBullish (self):
        if self.open > self.close:
            return False
        
        if self.open < self.close:
            return True
        
        return None
        
    def candelSize(self):
        size=abs(self.high-self.low)
        return size
        
        
        
    def __str__(self):
        return f"{self.ticker},{self.date},{self.time},{self.open},{self.high},{self.low},{self.close}"

class Candels:
    def __init__(self):
        self.candels=[]
        self.name=None
        
        
        
            
    def load_txt(self,filename):
        with open(filename) as f:         
            f.readline()
            t0=time.time()
            cero=False
            for line in f:
                line=line.strip()
                tokens=line.split(",")
                tokens[2]=int(tokens[2])
                date=tokens[1][:4]+"-"+tokens[1][4:6]+"-"+tokens[1][6:]
                if cero or tokens[2]==0:
                    cero=True
                    candel=Candel(tokens[0],date,tokens[2],tokens[3],tokens[4],tokens[5],tokens[6])
                    self.candels.append(candel)
            
            t1=time.time()
            print(t1-t0)
            self.name=self.candels[0].ticker
    
    def __str__(self):
        ss=""
        ss+="TICKER , DATE , TIME , OPEN , HIGH , LOW , CLOSE\n"
        
        for i in self.candels:
            ss+=str(i)
            ss+="\n"
        
        return ss
        
    def candel_size(self):
        l=[]
        for i in self.candels:
            size=i.close-i.open
            l.append(size)
            
        return l
    
  
    def changeTimeframe(self,series):
        #se estan transformando las velas de un minuto a la serie requerida
        #1d, 4h, 1h,5m
        timeFrame={"1d":60*24,"4h":60*4,"1h":60,"5m":5 }
        times=timeFrame[series]
        NewCandels=Candels()
        
        name=self.name
        while times<=len(self.candels):
            highs=[]
            lows=[]
            Open=self.candels[times-timeFrame[series]].open
            Close=self.candels[times].close
            time=self.candels[times-timeFrame[series]].time
            date=self.candels[times-timeFrame[series]].date
            for i in self.candels[times-timeFrame[series]:times]:
                highs.append(i.high)
                lows.append(i.low)
            times=times+timeFrame[series]
            NewCandels.candels.append(Candel(name,date,time,Open,max(highs),min(lows),Close))
            
        
        return NewCandels
            
        
        
    
    def flex(self):
        pass
    
    def table(self,x):
        Kandels=self.candels[-x:]
        newCandels=[]
        
        for j in Kandels:
            candel=[j.date , j.time , j.open , j.high , j.low, j.close,j.size,j.bullish]
            newCandels.append(candel)
        return newCandels
        
        
          
        
class Entorno:
    #candel 0 seria el posible POI
    #la distancia seria el radio en los cuales el candel 1 tendria que estar
    def __init__(self,canadel_0,canadel_1,distancia):
       self.canadel_0=canadel_0
       self.canadel_1=canadel_1
       self.delta=distancia
       self.inside=self.isInside()
       
    def isInside(self):
        k0=self.canadel_0
        k1=self.canadel_1
        diferencia=(k0-k1)
        return abs(diferencia)<self.delta
    

        

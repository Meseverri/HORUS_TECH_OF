import pandas as pd
import sys
sys.path.append("C:/Users/Raul Sampedro/Desktop/Horus Capital/HORUS TECHNOLOGIES/cAlgo")
from Candels import Candels


USDCAD=Candels()
USDCAD.load_txt("C:/Users/Raul Sampedro/Desktop/Horus Capital/HORUS TECHNOLOGIES/cAlgo/USDCAD.csv") 
USDCAD.changeTimeframe("5m")
ind=["date" , "time" , "open" , "high" , "low", "close","size","bullish"]
for i in USDCAD.changeTimeframe("1d").table(100):
    print(i)
    
USDCAD_df=pd.DataFrame(USDCAD.changeTimeframe("1d").table(100),columns=ind)
USDCAD_df
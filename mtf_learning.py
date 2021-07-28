import MetaTrader5 as mt5
import pandas as pd
# mostramos los datos sobre el paquete MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# establecemos la conexión con el terminal MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# conectamos con la cuenta indicando la contraseña y el servidor
authorized=mt5.login(764445, password="jxoerhf3")
if authorized:
    account_info=mt5.account_info()
    if account_info!=None:
        # mostramos como son los datos sobre la cuenta
        print(account_info)
        # mostramos los datos sobre la cuenta comercial en forma de diccionario
        print("Show account_info()._asdict():")
        account_info_dict = mt5.account_info()._asdict()
        for prop in account_info_dict:
            print("  {}={}".format(prop, account_info_dict[prop]))
        print()
 
       # transformamos el diccionario en DataFrame y lo imprimimos
        df=pd.DataFrame(list(account_info_dict.items()),columns=['property','value'])
        print("account_info() as dataframe:")
        print(df)
else:
    print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =",mt5.last_error())
 
# finalizamos la conexión con el terminal MetaTrader 5
mt5.shutdown()
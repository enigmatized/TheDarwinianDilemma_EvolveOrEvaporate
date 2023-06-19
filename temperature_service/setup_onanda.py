from collections import defaultdict
import requests
from time import sleep



from   urllib.error import HTTPError
import json

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import re
from datetime import datetime, timedelta, time

"""
SO get tokens
call exchange
clean data
format data correctly into pandas
return df

"""



def getBearAndAccount():    
    with open('bearTokenAndAccountInfo.json', 'r') as openfile:
        # Reading from json file
        oauthInfo = json.load(openfile)
    
    bearerTokenOanda = oauthInfo["bearer"]
    accountNumOanda  = oauthInfo["account"] 

    return (bearerTokenOanda, accountNumOanda)




def getCandles_fromOanada(currency = 'AUD_USD', count = "30", time= "5",  bearerToken = None, accountNum = None):
    try:
        r = requests.get('https://api-fxtrade.oanda.com/v3/instruments/'+currency +'/candles?count='+ str(count) +'&price=M&granularity=M'+time,
            headers= { 'Content-Type': 'application/json','Authorization': 'Bearer ' + bearerToken}
            )
        r.raise_for_status()
        print("Success, api request good, delete for debug")
        return (r.json(), True)
    #except HTTPError as http_err:
    #    print(f'HTTP error occurred: {http_err}')
    #    print(http_err.response.text)
    except Exception as err:
        print(f'Other error occurred  in function getCandles_fromOanada: {err}')
    
    print("failed")
    return ("", False)



def createPandasDfFromAPI(json_of_currency):

  dict_time_to_json_info_canldes     = prep_json_from_API_for_pandas(json_of_currency)

  mainDf                             = pd.DataFrame(dict_time_to_json_info_canldes).T
  #mainDf['heikin_ashi_open']  = 0.5 *( mainDf['close'].shift(1) +mainDf['open'].shift(1) ) 
  
  #Get rid of the first value that is NA as a result of the above operation
  mainDf       = mainDf.tail(-1) 

  return mainDf


#TODO there should be a unit test for this
def prep_json_from_API_for_pandas(json_Instrument_Info):
        innderDict = defaultdict(dict)
        
        inst    = json_Instrument_Info['instrument']
        grans   = json_Instrument_Info['granularity']
        candles = json_Instrument_Info['candles']
        #time_to_subtract = datetime.strptime("4:00:00", "%H:%M:%S")

        for x in candles:
            if x["complete"]:
                strObjDate = x["time"]
                time_Of_this_Candle = datetime.strptime(strObjDate[:19], '%Y-%m-%dT%H:%M:%S')
                innderDict[time_Of_this_Candle]["close"]               = float(x["mid"]['c'])
                innderDict[time_Of_this_Candle]["open"]                = float(x["mid"]['o'])
                innderDict[time_Of_this_Candle]["high"]                = float(x["mid"]['h'])
                innderDict[time_Of_this_Candle]["low"]                 = float(x["mid"]['l'])
                innderDict[time_Of_this_Candle]["heikin_ashi_close"]   = 0.25 * (float(x["mid"]['o']) + float(x["mid"]['c']) + float(x["mid"]['l']) + float(x["mid"]['h']))
                innderDict[time_Of_this_Candle]["volume"]              = int(x["volume"])
                innderDict[time_Of_this_Candle]["time"]                = (time_Of_this_Candle - timedelta(hours=4)).time() 
                innderDict[time_Of_this_Candle]['estTime']             = innderDict[time_Of_this_Candle]["time"] #TODO this should probably be made more correctly This may effect stats from my analysis in the end
                innderDict[time_Of_this_Candle]['timeOnly']            = innderDict[time_Of_this_Candle]["time"] #TODO this should probably be made more correctly

        return innderDict




def get_onanda_pandas_df(time="5"):
    (bearerTokenOanda, accountNumOanda) = getBearAndAccount()
    onanda_json_output = getCandles_fromOanada("AUD_USD", "30", str(time), bearerTokenOanda, accountNumOanda)
    #probably should do proper error handling here, #TODO
    onanda_df = createPandasDfFromAPI(onanda_json_output[0])
    return onanda_df

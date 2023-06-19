import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import defaultdict
from setup_onanda import * 




def make_RSI_df(df):
    # Generate the plot
    #df = pd.read_csv ('OANDAAUDUSD5min.csv')
    #df = df.reset_index()


    df['closeDelta']  = ( df['close'] - df['close'].shift(1) )
    #Remove NA row
    df = df.tail(-1)




    # Assuming you have a DataFrame called 'df' with a 'close' column

    # Calculate the price changes
    df['price_change'] = df['close'].diff()

    # Calculate the positive and negative price changes
    df['gain'] = df['price_change'].apply(lambda x: x if x > 0 else 0)
    df['loss'] = df['price_change'].apply(lambda x: abs(x) if x < 0 else 0)

    # Calculate the average gain and average loss over the desired period
    period = 14
    df['avg_gain'] = df['gain'].rolling(window=period).mean()
    df['avg_loss']       =   df['loss'].rolling(window=period).mean()

    # Calculate the relative strength (RS)
    df['RS'] = df['avg_gain'] / df['avg_loss']

    # Calculate the relative strength index (RSI)
    df['RSI']  = df['RS'].apply(lambda x : 100 - (100 / (1 + x)) )

    # Print the RSI values
    # Remove the first 14 rows from the DataFrame
    df = df.iloc[14:]

    # Convert the index to a DatetimeIndex
    df.index = pd.to_datetime(df.index)
    return df














def make_RSI_lookup(df):
    # Create the probability of future projection from pandas df
    for i in range(1, 11):
        df['P/L' +str(i) +'Short']  = ( df['close'] - df['close'].shift(-i) )
        df['P/L' +str(i) +'Long']  =  (  df['close'].shift(-i) - df['close']     )
    ddict_of_ddict = defaultdict(lambda: defaultdict(list))

    df = df.iloc[11:]
    df = df.iloc[:-11]

    count = 1
    for index, row in  df.iterrows():
        if count  > 14:
            for i in range(1, 11):
                ddict_of_ddict['P/L' +str(i) +'Long'][int(row['RSI'])].append(row['P/L' +str(i) +'Long'])
                ddict_of_ddict['P/L' +str(i) +'Short'][int(row['RSI'])].append(row['P/L' +str(i) +'Short'])
        count +=1


    return ddict_of_ddict



def onanda_rsi_value_to_int(time = "5"):
    return int(make_RSI_df(get_onanda_pandas_df(time)).tail(1)['RSI'])



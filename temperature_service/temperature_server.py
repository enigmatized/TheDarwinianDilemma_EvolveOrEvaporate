import random
from flask import Flask, make_response, render_template, g
import matplotlib.pyplot as plt
import pandas as pd
import io
import numpy as np
from collections import defaultdict
from itertools   import chain
import os
import regex as re


from  display_rsi_image import *
from  setup_onanda      import *
from  rsi_df_helpers    import * 

#Create RSI lookup table
CSVfiles = []
for file in os.listdir("./"): 
  if file.endswith(".csv"): 
    CSVfiles.append(file)


allDfs   = {}
allDKeys = []
for x in CSVfiles:
  minInterval = int(int(re.search('[0-9]+', x).group())) ## Note this does not work for futures
  #minInterval = int(x.replace(".csv", "")[-1]) #This only works for futures
  temp_df = pd.read_csv (x)
  allDfs[minInterval] = make_RSI_lookup(make_RSI_df(temp_df))  
  print("minInterval", minInterval, "to ", x)
  allDKeys.append(minInterval)




ddict_of_ddict =  make_RSI_lookup(make_RSI_df(pd.read_csv('OANDAAUDUSD5min.csv')))



app = Flask(__name__)


@app.route('/aboutME')
def aboutMe():
    return render_template('index.html')


@app.route('/')
def get_temperature():
    temperature_c = random.randint(-10, 33)
    return { 'temperature_c': temperature_c }

@app.route('/plot')
def serve_plot():
# Generate the plot
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
# Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

# Create a response and set the appropriate headers
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


#def make_RSI_df(df):
#    # Generate the plot
#    #df = pd.read_csv ('OANDAAUDUSD5min.csv')
#    #df = df.reset_index()
#    
#    
#    df['closeDelta']  = ( df['close'] - df['close'].shift(1) )
#    #Remove NA row
#    df = df.tail(-1)
#    
#    
#    
#    
#    # Assuming you have a DataFrame called 'df' with a 'close' column
#    
#    # Calculate the price changes
#    df['price_change'] = df['close'].diff()
#    
#    # Calculate the positive and negative price changes
#    df['gain'] = df['price_change'].apply(lambda x: x if x > 0 else 0)
#    df['loss'] = df['price_change'].apply(lambda x: abs(x) if x < 0 else 0)
#    
#    # Calculate the average gain and average loss over the desired period
#    period = 14
#    df['avg_gain'] = df['gain'].rolling(window=period).mean()
#    df['avg_loss']       =   df['loss'].rolling(window=period).mean()
#    
#    # Calculate the relative strength (RS)
#    df['RS'] = df['avg_gain'] / df['avg_loss']
#    
#    # Calculate the relative strength index (RSI)
#    df['RSI']  = df['RS'].apply(lambda x : 100 - (100 / (1 + x)) )
#    
#    # Print the RSI values
#    # Remove the first 14 rows from the DataFrame
#    df = df.iloc[14:]
#    
#    # Convert the index to a DatetimeIndex
#    df.index = pd.to_datetime(df.index)
#    return df
#
#
#
#
#
#def make_RSI_lookup(df):
#    # Create the probability of future projection from pandas df
#    for i in range(1, 11):
#        df['P/L' +str(i) +'Short']  = ( df['close'] - df['close'].shift(-i) )
#        df['P/L' +str(i) +'Long']  =  (  df['close'].shift(-i) - df['close']     )
#    ddict_of_ddict = defaultdict(lambda: defaultdict(list))
#
#    df = df.iloc[11:]
#    df = df.iloc[:-11]
#
#    count = 1
#    for index, row in  df.iterrows():
#        if count  > 14:
#            for i in range(1, 11):
#                ddict_of_ddict['P/L' +str(i) +'Long'][int(row['RSI'])].append(row['P/L' +str(i) +'Long'])
#                ddict_of_ddict['P/L' +str(i) +'Short'][int(row['RSI'])].append(row['P/L' +str(i) +'Short'])
#        count +=1
#
#
#    return ddict_of_ddict
#
#
#
#def onanda_rsi_df():
#    return int(make_RSI_df(get_onanda_pandas_df()).tail(1)['RSI'])
#

@app.route('/manyRSI')
def rsi_many():
    return rsi_image_gen(allDfs)





@app.route('/rsi')
def rsi_():
    #Need to call onanda

    #need to make onanda df

    #Need to look up RSI num


    probabilites      =  []
    averageFromTrade  =  [] 

    #Function to provide tuple of index, and rsi int to get list of values from dictionary
    getRSIVal =  lambda ind_and_rsi_int_val : ddict_of_ddict['P/L' +str(ind_and_rsi_int_val[0]) +'Long'][ind_and_rsi_int_val[1]]
    getRSIVals = lambda ls_of_tuples_vals :  list(map( getRSIVal, ls_of_tuples_vals))
     

    fig, ax = plt.subplots(2)
    for i in range(1, 11):

        #Get RSI value
        rsi_value_as_int = onanda_rsi_value_to_int()

        #if appropiate, average the RSI
        if rsi_value_as_int > 2 and rsi_value_as_int < 98:#TODO handle better case here
            #Format data for function
            ls_of_tuples = zip([i , i, i ], [rsi_value_as_int - 1, rsi_value_as_int , rsi_value_as_int+1] ) 
            #return all values as one list
            ls_values = list(chain.from_iterable(getRSIVals(ls_of_tuples)))
            val = len([x for x in ls_values if x > 0]) / len(ls_values)
            probabilites.append(val)
            #Average probability
            averageFromTrade.append( sum(ls_values)/len(ls_values))
        else:
            #Get value of Probabilites
            v = ddict_of_ddict['P/L' +str(i) +'Long'][rsi_value_as_int]
            val = len([x for x in v if x > 0]) / len(v)
            probabilites.append(val)
    
            #Average probability 
            averageFromTrade.append( sum(v)/len(v))



    # Generate x-axis values (assuming equal spacing)
    x = range(1, len(probabilites)+1)

    # Plot the line graph
    ax[0].plot(x, probabilites, marker='o', linestyle='-', color='blue')
    ax[1].plot(x, averageFromTrade, marker='o', linestyle='-', color='blue')
    
    # Add labels and title
    ax[0].set_xlabel('Period forward from now')
    ax[1].set_xlabel('Period forward from now')
    ax[0].set_ylabel('Probability of a profit')
    ax[1].set_ylabel('Average profit/loss from trade taken now')
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.3, hspace=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response




if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')

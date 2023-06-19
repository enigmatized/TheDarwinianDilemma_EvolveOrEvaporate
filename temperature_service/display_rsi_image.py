import random
import matplotlib.pyplot as plt
import pandas as pd
import io
import numpy as np
from collections import defaultdict
from itertools   import chain
import os
import regex as re

from  setup_onanda      import *
from  rsi_df_helpers    import *

from flask import  make_response 

def rsi_image_gen(dict_of_dicts):

    #List of possible of markers for plot
    markers = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd']
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    #Function to provide tuple of index, and rsi int to get list of values from dictionary

    #Create for three displays 1) Probability of profit, 2) average profit if taken 3) EV
    fig, ax = plt.subplots(3)
    for j, (k, dict_of_ls)  in enumerate(dict_of_dicts.items()):
            
        getRSIVal =  lambda ind_and_rsi_int_val : dict_of_ls['P/L' +str(ind_and_rsi_int_val[0]) +'Long'][ind_and_rsi_int_val[1]]
        
        getRSIVals = lambda ls_of_tuples_vals :  list(map( getRSIVal, ls_of_tuples_vals))


        averageFromTrade  =  []
        probabilites      =  []
        ev_values         =  []
        for i in range(1, 11):
    
            #Get RSI value
            rsi_value_as_int = onanda_rsi_value_to_int(k)
    
            #if appropiate, average the RSI
            if rsi_value_as_int > 2 and rsi_value_as_int < 98:#TODO handle better case here
                #Format data for function
                ls_of_tuples = zip([i , i, i ], [rsi_value_as_int - 1, rsi_value_as_int , rsi_value_as_int+1] )
                #return all values as one list
                ls_values = list(chain.from_iterable(getRSIVals(ls_of_tuples)))
                
                #split trades
                all_postive_trades =  [x for x in ls_values if x > 0]
                all_negative_trades = [x for x in ls_values if x < 0]
                
                #
                val = len(all_postive_trades) / len(ls_values)
                probabilites.append(val)
                
                #Average probability
                averageFromTrade.append( sum(ls_values)/len(ls_values))
                
                #
                average_ = lambda ls1 : sum(ls1)/len(ls1)
                chance_of_negative_trade = 1 - val
                ev = (chance_of_negative_trade * average_(all_negative_trades) ) + (val * average_(all_postive_trades)) 
                ev_values.append(ev)

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
        ax[0].plot(x, probabilites, marker=markers[j], linestyle='-', color=colors[j])
        ax[1].plot(x, averageFromTrade, marker=markers[j], linestyle='-', color=colors[j])
        ax[2].plot(x, ev_values, marker=markers[j], linestyle='-', color=colors[j])
    
    # Add labels and title
    ax[0].set_xlabel('Period forward from now')
    ax[1].set_xlabel('Period forward from now')
    ax[0].set_ylabel('Probability of a profit')
    ax[1].set_ylabel('Average profit/loss from trade taken now')
    ax[1].set_ylabel('EV of trade, if the stop loss was the time/period')
    ax[0].legend(list(map((lambda key_ : "time period " + str(key_)), list(dict_of_dicts.keys())  )))
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.3, hspace=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


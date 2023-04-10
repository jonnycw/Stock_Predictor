# needed for API
import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader as pdr
import yfinance as yfin
yfin.pdr_override()
from dotenv import load_dotenv
import os
import json
import requests

def get_econ_data ():
    # define data for DataReader
    end = dt.date.today()
    start= end - dt.timedelta(days=365*21)
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')

    # select tables, enter as dataframe
    econ_df = pdr.DataReader(['GDPC1','UNRATE','DFF','EFFR','MORTGAGE30US','DTB3','PRIME','MICH','TOTALSA','UMCSENT','HOUST','RECPROUSM156N','REAINTRATREARAT1YE','REAINTRATREARAT10Y'], 'fred', start_str, end_str)
    names = ['real gdp','unemployment','fed fund effective rate', 'effective fed fund rate', '30 year mortgage', '3t-bill market rate', 'prime bank loan rate', 'michigan inflaction pred', 'total car sales','cons sentiment','new housing','recession prob']
    
    #filling blank values with prior value
    econ_df.fillna(method='ffill', inplace=True)
    # calculate pct change
    econ_df2 = econ_df.pct_change()
    econ_df2['RECPROUSM156N']=econ_df['RECPROUSM156N']
    econ_df = econ_df2
    # seporate out daily metrics
    daily_df = econ_df[['DFF', 'EFFR', 'DTB3']]
    econ_df = econ_df.drop(columns=['DFF', 'EFFR', 'DTB3'])
    # replace 0 values with null
    econ_df.replace(0, np.nan, inplace=True)
    # refill nulls with prior value
    econ_df.fillna(method='ffill', inplace=True)
        # add back in daily values
    econ_df = pd.concat([daily_df, econ_df], axis=1)
    # remove inf values
    econ_df[np.isinf(econ_df)] = 0
    # update index to date
    econ_df.index = econ_df.index.date

    return econ_df
# General packages
import pandas as pd
import numpy as np
import hvplot.pandas
import datetime as dt

# needed for API
import pandas_datareader as pdr
import yfinance as yfin
yfin.pdr_override()
import requests

#turn off warning signs for cleaner code
from warnings import filterwarnings
filterwarnings("ignore")

def spy_analysis ():
    import datetime as dt
    # Set up timeframe for model
    end = dt.date.today()
    start= end - dt.timedelta(days=365*20)
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')
    
    # set API pull to SPY
    spy = 'SPY'
    df = pdr.data.get_data_yahoo(spy, start=start_str, end=end_str)
    spy_df = pd.DataFrame()
    spy_df['spy_close'] = df[["Adj Close"]]
    spy_df['spy_change'] = spy_df['spy_close'].pct_change()
    spy_df = spy_df.dropna()
    
    # SPY movement indicators
    spy_df['up_down'] = np.where(spy_df['spy_change']>0,0,1)
    spy_df['spy_con_direction'] = (spy_df.groupby(spy_df['up_down'].ne(spy_df['up_down'].shift()).cumsum()).cumcount()+1)*np.where(spy_df['spy_change']>=0,1,-1)
    spy_df = spy_df.drop(columns=['up_down'])
    spy_df['3_day_change'] = ((spy_df['spy_change']+1).rolling(window=3).apply(np.prod, raw=True)-1)
    spy_df['15_day_change'] = ((spy_df['spy_change']+1).rolling(window=15).apply(np.prod, raw=True)-1)
    spy_df['45_day_change'] = ((spy_df['spy_change']+1).rolling(window=45).apply(np.prod, raw=True)-1)
    spy_df['90_day_change'] = ((spy_df['spy_change']+1).rolling(window=90).apply(np.prod, raw=True)-1)
    spy_df['15_day_stdv'] = spy_df['spy_change'].rolling(window=15).std()
    spy_df['30_day_stdv'] = spy_df['spy_change'].rolling(window=30).std()
    spy_df['60_day_stdv'] = spy_df['spy_change'].rolling(window=60).std()
    spy_df['4sma_pct_price'] = (spy_df['spy_close'].rolling(window=4).mean()/spy_df['spy_close']) - 1
    spy_df['30sma_pct_price'] = (spy_df['spy_close'].rolling(window=30).mean()/spy_df['spy_close']) - 1
    spy_df['100sma_pct_price'] = (spy_df['spy_close'].rolling(window=100).mean()/spy_df['spy_close']) - 1
    spy_df['bolling_top_pct'] = ((spy_df['spy_close'].rolling(window=60).mean()+spy_df['spy_close'].rolling(window=60).std()*2)/spy_df['spy_close']) - 1
    spy_df['bolling_bot_pct'] = ((spy_df['spy_close'].rolling(window=60).mean()-spy_df['spy_close'].rolling(window=60).std()*2)/spy_df['spy_close']) - 1
    spy_df.index = spy_df.index.date
    
    # return results
    return spy_df

spy_df = spy_analysis()
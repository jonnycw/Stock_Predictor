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

def vix_analysis ():
    # Set up timeframe for model
    end = dt.date.today()
    start= end - dt.timedelta(days=365*20)
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')
    
    # set API pull to vix
    vix = '^VIX'
    df = pdr.data.get_data_yahoo(vix, start=start_str, end=end_str)
    vix_df = pd.DataFrame()
    vix_df['vix_close'] = df[["Close"]]
    vix_df['vix_change'] = vix_df['vix_close'].pct_change()
    vix_df = vix_df.dropna()
    
    # convert data to numpy to be scaled
    x_raw = vix_df["vix_close"].to_numpy()
    x_raw = np.reshape(x_raw, [-1,1])
    
    # scale the data
    scaler = StandardScaler().fit(x_raw)
    x_scaled = scaler.transform(x_raw)
    
    # cluster the data
    cluster_model = KMeans(n_clusters=3, random_state=0).fit(x_scaled)
    vix_df['labels']=cluster_model.labels_

    # indicate how long the VIX has been in it's current state
    vix_df['vix_days_in_label'] = vix_df.groupby(vix_df['labels'].ne(vix_df['labels'].shift()).cumsum()).cumcount()+1
    vix_df['up_down'] = np.where(vix_df['vix_change']>=0,1,-1)
    vix_df['vix_con_direction'] = (vix_df.groupby(vix_df['up_down'].ne(vix_df['up_down'].shift()).cumsum()).cumcount()+1)*vix_df['up_down']
    vix_df = vix_df.drop(columns=['up_down'])
    vix_df.index = vix_df.index.date
    
    # return results
    return vix_df, cluster_model
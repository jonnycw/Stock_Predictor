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
    spy_df['volume'] = df[["Volume"]]
    spy_df['high'] = df[["High"]]
    spy_df['low'] = df[["Low"]]
    spy_df['spy_change'] = spy_df['spy_close'].pct_change()
    spy_df['volume_change'] = spy_df['volume'].pct_change()
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
    spy_df['volume_pct_avg'] = (spy_df['volume']/spy_df['volume'].rolling(window=30).mean()) - 1
    spy_df['daily_fibonacci'] = (spy_df['spy_close']-spy_df['low'])/(spy_df['high']-spy_df['low'])
    spy_df['daily_fibonacci%'] = spy_df['daily_fibonacci'].pct_change()
    spy_df['weekly_fibonacci'] = (spy_df['spy_close']-spy_df['low'].rolling(window=7).min())/(spy_df['high'].rolling(window=7).max()-spy_df['low'].rolling(window=7).min())
    spy_df.index = spy_df.index.date
    
    # Calculate the Relative Strength Index (RSI) for the stock's price
    def relative_strength_index(spy_df):
        delta = spy_df['spy_close'].diff()
        up_days = delta.where(delta > 0, 0)
        down_days = abs(delta.where(delta < 0, 0))
        avg_gain = up_days.rolling(window=14).mean()
        avg_loss = down_days.rolling(window=14).mean()
        rs = avg_gain / avg_loss                                                                               
        spy_df['rsi'] = 100 - (100 / (1 + rs))
        return spy_df
    spy_df = relative_strength_index(spy_df)
    
    # Calculate the Stochastic Oscillator for the stock's price
    def stochastic_oscillator(spy_df):
        high_14, low_14 = spy_df['high'].rolling(window=14).max(), spy_df['low'].rolling(window=14).min()
        spy_df['%K'] = (spy_df['spy_close'] - low_14) / (high_14 - low_14) * 100
        spy_df['%D'] = spy_df['%K'].rolling(window=3).mean()
        return spy_df
    spy_df = stochastic_oscillator(spy_df)
    
    def macd(spy_df):
        spy_df['ma12'] = spy_df['spy_close'].ewm(span=12).mean()
        spy_df['ma26'] = spy_df['spy_close'].ewm(span=26).mean()
        spy_df['macd'] = spy_df['ma12'] - spy_df['ma26']
        spy_df['signal_line'] = spy_df['macd'].ewm(span=9).mean()
        return spy_df
    spy_df = macd(spy_df)
                             
    # Calculate the Commodity Channel Index (CCI) for the stock's price
    def commodity_channel_index(spy_df):
        typical_price = (spy_df['high'] + spy_df['low'] + spy_df['spy_close']) / 3
        sma = typical_price.rolling(window=20).mean()
        mean_deviation = abs(typical_price - sma).rolling(window=20).mean()
        spy_df['cci'] = (typical_price - sma) / (0.015 * mean_deviation)
        return spy_df
    spy_df = commodity_channel_index(spy_df)
                             
    # Calculate the Williams %R for the stock's price
    def williams_percent_r(spy_df):
        highest_high = spy_df['high'].rolling(window=14).max()
        lowest_low = spy_df['low'].rolling(window=14).min()
        spy_df['%r'] = -100 * (highest_high - spy_df['spy_close']) / (highest_high - lowest_low)
        return spy_df
    spy_df = williams_percent_r(spy_df)
    
    # drop values that are directly relative
    spy_df = spy_df.drop(columns=['ma12', 'ma26', 'macd','high','low'])
    spy_df['y'] = spy_df['spy_change'].shift(-1)
                                                                                               
    # return results
    return spy_df
# General packages
import pandas as pd
import numpy as np
import hvplot.pandas
import datetime as dt

# Sentiment Score
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.request import urlopen
from urllib.request import Request
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def market_sent ():
    # define variables for function
    ticker = 'SPY'
    web_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}
    
    
    # set up request
    url = web_url + ticker
    req = Request(url=url,headers={"User-Agent": "Chrome"}) 
    response = urlopen(req)    
    html = BeautifulSoup(response,"html.parser")
    news_table = html.find(id='news-table')
   
    # Pull articles to new dataframe
    parsed_news = []
    for x in news_table.findAll('tr'):
        a_element = x.find('a', class_='tab-link-news')
        if a_element is not None:
            text = a_element.get_text()
            date_scrape = x.td.text.split()
            if len(date_scrape) == 1:
                time = date_scrape[0]
            else:
                date = date_scrape[0]
                time = date_scrape[1]
            parsed_news.append([date, time, text])
        
    # Sentiment Analysis portion
    analyzer = SentimentIntensityAnalyzer()

    columns = ['Date', 'Time', 'Headline']
    news = pd.DataFrame(parsed_news, columns=columns,)
    scores = news['Headline'].apply(analyzer.polarity_scores).to_list()

    df_scores = pd.DataFrame(scores)
    news = news.join(df_scores, rsuffix='_right')
    news['Date'] = pd.to_datetime(news['Date'])
    news = news.set_index('Date')
    
    # make final table for that show average sentiment for each day 
    sentiment_df = pd.DataFrame()
    sentiment_df = news.groupby(news.index).mean()
    sentiment_df = sentiment_df[['compound']]
    sentiment_df = sentiment_df.rename(columns={'compound': 'Sentiment'})
    sentiment_df.index = sentiment_df.index.date
    
    return sentiment_df